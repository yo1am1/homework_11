import datetime
import decimal

import currencyapicom
import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import RateForm
from .models import Rate


class DecimalAsFloatJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


def index(request):
    current_date = datetime.date.today()
    current_rates = list(
        Rate.objects.values("vendor", "currency_a", "currency_b")
        .filter(date=current_date)
        .order_by("vendor")
    )
    return JsonResponse(
        {"current_rates": current_rates}, encoder=DecimalAsFloatJSONEncoder
    )


def add_param(request):
    if request.method == "POST":
        form = RateForm(request.POST)

        if form.is_valid():
            form.date = datetime.date.today()
            form.save()
            return HttpResponseRedirect(reverse("calculate"))
    else:
        form = RateForm()
    context = {"form": form}
    return render(request, "index.html", context)


def display(request):
    if request.method == "POST":
        if "display_buy" in request.POST:
            form = RateForm(request.POST)
            print(Rate.currency_a)
            if form.is_valid():
                form.save()
                filt = (
                    Rate.objects.filter(currency_a=f"{form.cleaned_data['currency_a']}")
                    .values()
                    .order_by("buy", descending=True)
                    .first()
                )
                return render(request, "index.html", {"filt": filt})
        elif "display_sell" in request.POST:
            form = RateForm(request.POST)
            if form.is_valid():
                form.save()
                filt = (
                    Rate.objects.filter(currency_a=f"{form.cleaned_data['currency_a']}")
                    .values()
                    .order_by("sell", ascending=True)
                    .first()
                )
                return render(request, "index.html", {"filt": filt})
    return render(request, "index.html")


def vkurse(request):
    r = requests.get("https://vkurse.dp.ua/course.json")
    answer = r.json()

    return JsonResponse(answer, encoder=DecimalAsFloatJSONEncoder, safe=False)


def currencyapi(request):
    client = currencyapicom.Client("YQeLH52G55DlV361wbi6Vs1cDj3Jg0TG2KTSBIG6")
    result = client.latest()

    return JsonResponse(result, encoder=DecimalAsFloatJSONEncoder)


def nbu(request):
    r = requests.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    )
    answer = r.json()

    return JsonResponse(answer, encoder=DecimalAsFloatJSONEncoder, safe=False)

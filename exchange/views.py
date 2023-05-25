import datetime
import decimal

import currencyapicom
import requests
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render

from .forms import ExchangeForm
from .models import Rate


class DecimalAsFloatJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


def index(request):
    current_date = datetime.date.today()
    current_rates = list(
        Rate.objects.filter(date=current_date)
        .values("vendor", "currency_a", "currency_b", "sell", "buy")
        .order_by("vendor")
    )
    if current_rates:
        context = {
            "all": current_rates,
        }
    else:
        context = {"all": "No data"}
    return render(request, "display.html", context)


def display(request):
    current_date = datetime.date.today()

    form = ExchangeForm(request.POST)
    if request.method == "POST" and form.is_valid():
        if "USD to UAH" in request.POST:
            num = form.cleaned_data["amount"]
            current_rates = (
                Rate.objects.filter(date=current_date, currency_a="USD")
                .all()
                .values()
                .order_by("buy")
            )
            cof, vendor = (
                list(current_rates)[-1]["buy"],
                list(current_rates)[-1]["vendor"],
            )
            result = round(num * float(cof), 2)
            return render(
                request, "index.html", {"vendor": f"Розрахунок: {result}", "form": form}
            )

        elif "EUR to UAH" in request.POST:
            num = form.cleaned_data["amount"]
            current_rates = (
                Rate.objects.filter(date=current_date, currency_a="EUR")
                .all()
                .values()
                .order_by("buy")
            )
            cof, vendor = (
                list(current_rates)[-1]["buy"],
                list(current_rates)[-1]["vendor"],
            )
            result = round(num * float(cof), 2)
            return render(
                request, "index.html", {"vendor": f"Розрахунок: {result}", "form": form}
            )

        elif "UAH to USD" in request.POST:
            num = form.cleaned_data["amount"]
            current_rates = (
                Rate.objects.filter(date=current_date, currency_a="USD")
                .all()
                .values()
                .order_by("sell")
            )
            cof, vendor = (
                list(current_rates)[0]["sell"],
                list(current_rates)[0]["vendor"],
            )
            result = round(num * 1 / float(cof), 2)
            return render(
                request, "index.html", {"vendor": f"Розрахунок: {result}", "form": form}
            )

        elif "UAH to EUR" in request.POST:
            num = form.cleaned_data["amount"]
            current_rates = (
                Rate.objects.filter(date=current_date, currency_a="EUR")
                .all()
                .values()
                .order_by("sell")
            )
            cof, vendor = (
                list(current_rates)[0]["sell"],
                list(current_rates)[0]["vendor"],
            )
            result = round(num * 1 / float(cof), 2)
            return render(
                request, "index.html", {"vendor": f"Розрахунок: {result}", "form": form}
            )
    else:
        form = ExchangeForm()
        return render(request, "index.html", {"form": form})


# region JsonOutput
def privat(request):
    r = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
    answer = r.json()

    return JsonResponse(answer, encoder=DecimalAsFloatJSONEncoder, safe=False)


def monobank(request):
    r = requests.get("https://api.monobank.ua/bank/currency")
    answer = r.json()

    return JsonResponse(answer, encoder=DecimalAsFloatJSONEncoder, safe=False)


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


# endregion

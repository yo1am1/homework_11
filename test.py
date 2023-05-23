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
            if form.is_valid():
                form.save()
                filt = (
                    Rate.objects.filter(currency_a=f"{form.cleaned_data['currency_a']}")
                    .values()
                    .order_by("buy", descending=True)
                    .first()
                )
                context = {"filt": filt}
                return render(request, "index.html", context)
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
                context = {"filt": filt}
                return render(request, "index.html", context)
    return render(request, "index.html")

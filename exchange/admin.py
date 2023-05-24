from django.contrib import admin

from exchange.models import Rate


class RateAdmin(admin.ModelAdmin):
    list_display = ("date", "vendor", "currency_a", "currency_b", "sell", "buy")
    list_filter = ("date", "vendor", "currency_a", "currency_b")
    search_fields = ("date", "vendor", "currency_a", "currency_b")


admin.site.register(Rate, RateAdmin)

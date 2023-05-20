from django.db import models
from django.utils import timezone


# Create your models here.


class Rate(models.Model):
    date = models.DateField(default=timezone.now)
    vendor = models.CharField(max_length=255)
    currency_a = models.CharField(max_length=3)
    currency_b = models.CharField(max_length=3)
    sell = models.DecimalField(max_digits=15, decimal_places=10)
    buy = models.DecimalField(max_digits=15, decimal_places=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "vendor", "currency_a", "currency_b"],
                name="unique_rate",
            )
        ]


class Search(models.Model):
    currency_a = models.DecimalField(max_digits=15, decimal_places=10)
    currency_b = models.DecimalField(max_digits=15, decimal_places=10)
    date = models.DateField(default=timezone.now)

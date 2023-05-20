from django import forms

from .models import Search


class RateForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ["currency_a", "currency_b"]

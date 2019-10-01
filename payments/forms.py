import datetime
from django import forms


def get_year_choices():
    this_year = datetime.date.today().year
    return list(range(this_year, this_year - 10))


class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', required=True, decimal_places=2, max_value=1000, min_value=1,
                                max_digits=8)
    email = forms.EmailField(required=False)
    cellphone = forms.CharField(required=False, max_length=200)
    details = forms.CharField(label='Details', required=True, max_length=200)


class MobilePaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', required=True, decimal_places=2, max_value=1000, min_value=1,
                                max_digits=8)
    cellphone = forms.CharField(required=True, max_length=200)
    details = forms.CharField(label='Details', required=True, max_length=200)

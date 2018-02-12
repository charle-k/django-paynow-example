from django import forms
from django.forms.extras.widgets import SelectDateWidget

YEAR_CHOICES = ('2018', '2019', '2020', '2021', '2022', '2023', '2024' )


class MobilePaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', required=True, decimal_places=2,
                                max_value=1000, min_value=1, max_digits=8)
    cellphone = forms.IntegerField(label='Cellphone Number', required=True)
    reference = forms.CharField(label='Ref/Account', required=False,
                                max_length=200)


class DateSearchForm(forms.Form):
    day = forms.DateField(label='Jump to Date:',
                          required=True,
                          widget=SelectDateWidget(empty_label=("Choose Year",
                                                               "Choose Month",
                                                               "Choose Day"),
                                                  years=YEAR_CHOICES,),
                          )

import datetime
from django import forms

# YEAR_CHOICES = ('2018', '2019', '2020', '2021', '2022', '2023', '2024' )
def get_year_choices():
    this_year = datetime.date.today().year
    return list(range(this_year, this_year - 10))


class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', required=True, decimal_places=2, max_value=1000, min_value=1,
                                max_digits=8)
    email = forms.EmailField(required=True)
    details = forms.CharField(label='Details', required=True, max_length=200)



class DateSearchForm(forms.Form):
    day = forms.DateField(label='Jump to Date:',
                          required=True,
                          widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                                        years=get_year_choices),
                          )

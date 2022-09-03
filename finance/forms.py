import datetime

from django import forms

from finance.models import Payment

current_year = datetime.datetime.today().year
current_month = datetime.datetime.today().month

MONTH_SELECTION = (
    (datetime.date(current_year, 1, 1), 'January'),
    (datetime.date(current_year, 2, 1), 'February'),
    (datetime.date(current_year, 3, 1), 'March'),
    (datetime.date(current_year, 4, 1), 'April'),
    (datetime.date(current_year, 5, 1), 'May'),
    (datetime.date(current_year, 6, 1), 'June'),
    (datetime.date(current_year, 7, 1), 'July'),
    (datetime.date(current_year, 8, 1), 'August'),
    (datetime.date(current_year, 9, 1), 'September'),
    (datetime.date(current_year, 10, 1), 'October'),
    (datetime.date(current_year, 11, 1), 'November'),
    (datetime.date(current_year, 12, 1), 'December')
)

class CustomPaymentForm(forms.ModelForm):

    payment_for_month = forms.DateField(
        initial=datetime.date(current_year, current_month, 1),
        widget=forms.Select(choices=MONTH_SELECTION)
    )

    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['payment_id']

        
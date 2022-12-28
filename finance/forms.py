import datetime

from django import forms
from django.forms import DateInput
from django.core.exceptions import ValidationError

from finance.models import Payment
from finance.tasks import payment_mail

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
    send_payment_mail = forms.BooleanField(required=False)


    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['payment_id']
        widgets = {
            'invoice_date': DateInput(attrs={'type':'date'}),
            'payment_date': DateInput(attrs={'type':'date'})
        }
        labels = {
            'payment_id': 'Payment ID',
            'service': 'Service',
            'payment_for_month': 'Payment for Month',
            'payment_status': 'Payment Status',
            'amount': 'Amount',
            'invoice_no': 'Invoice No.',
            'invoice_doc': 'Invoice Doc.',
            'invoice_date': 'Invoice Date',
            'payment_date': 'Payment Date',
            'payment_mode': 'Payment Mode',
            'card_no': 'Card No.',
        }
    
    def __init__(self, *args, **kwargs):

        super(CustomPaymentForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            if key == 'invoice_doc':
                pass
            elif key == 'send_payment_mail':
                pass
            else:
                self.fields[key].widget.attrs.update({'class': 'payment-form-fields form-fields'})

    def save(self, commit=True):
        instance = super(CustomPaymentForm, self).save(commit=False)
        if self.cleaned_data['send_payment_mail'] is True:
            payment_mail.delay(instance.id)
        if commit:
            instance.save()
        return instance
    
    def clean(self):
        """
        If payment is paid, ensure payment related fields are submitted
        i.e., payment_date, payment_mode, inovice_doc etc.
        """
        cleaned_data = super().clean()
        is_paid = cleaned_data.get('payment_status', False)
        if is_paid and (
            not cleaned_data['invoice_no'] or not cleaned_data['invoice_doc']
            or not cleaned_data['invoice_date'] or not cleaned_data['payment_date']
            or not cleaned_data['payment_mode'] or not cleaned_data['card_no']
        ):
            raise ValidationError(
                "Please enter/attach all payment related information if the payment is 'Paid'"
            )

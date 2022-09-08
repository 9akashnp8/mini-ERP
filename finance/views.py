from sqlite3 import Date
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.forms import DateInput
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


from finance.models import Payment, Service
from finance.forms import CustomPaymentForm

#Helpers
def get_payment_amount(request):
    service = request.GET.get('service_id')
    amount = Service.objects.get(id=service).current_cost
    return HttpResponse(amount)

# Create your views here.
class PaymentListView(ListView):
    model = Payment
    context_object_name = 'payments'

class PaymentDetailView(DetailView):
    model = Payment
    context_object_name = 'payment'

class PaymentCreateView(CreateView):
    model = Payment
    form_class = CustomPaymentForm

class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = CustomPaymentForm

class PaymentDeleteView(DeleteView):
    model = Payment
    success_url = reverse_lazy('payment_list')

class ServiceListView(ListView):
    model = Service
    context_object_name = 'service'

class ServiceDetailView(DetailView):
    model = Service
    context_object_name = 'service'

class ServiceCreateView(CreateView):
    model = Service
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super(ServiceCreateView, self).get_form(form_class)
        
        # Custom Class for styling
        for key in form.fields:
            form.fields[key].widget.attrs.update({'class': 'service-form-fields form-fields'})

        # Better Labels
        form.fields['service_id'].label = 'Service ID'
        form.fields['category'].label = 'Category'
        form.fields['platform'].label = 'Platform'
        form.fields['end_user'].label = 'End User'
        form.fields['payment_interval'].label = 'Payment Interval'
        form.fields['current_cost'].label = 'Current Cost'
        form.fields['estimated_due_date'].label = 'Next Due Date'
        form.fields['status'].label = 'Service Status'

        form.fields['estimated_due_date'].widget = DateInput(attrs={'type': 'date', 'class': 'service-form-fields form-fields'})

        return form

class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super(ServiceUpdateView, self).get_form(form_class)

        # Custom class for styling
        for key in form.fields:
            form.fields[key].widget.attrs.update({'class': 'service-form-fields form-fields'})

        # Better Labels
        form.fields['service_id'].label = 'Service ID'
        form.fields['category'].label = 'Category'
        form.fields['platform'].label = 'Platform'
        form.fields['end_user'].label = 'End User'
        form.fields['payment_interval'].label = 'Payment Interval'
        form.fields['current_cost'].label = 'Current Cost'
        form.fields['estimated_due_date'].label = 'Next Due Date'
        form.fields['status'].label = 'Service Status'

        # Date Input
        form.fields['estimated_due_date'].widget = DateInput(attrs={'type': 'date', 'class': 'service-form-fields form-fields'})

        return form

class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('service_list')

def service_payments_view(request, pk):
    payments = Payment.objects.filter(service=pk)
    context = {'payments': payments}
    return render(request, 'finance/payment_list.html', context)
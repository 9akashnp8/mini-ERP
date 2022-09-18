from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
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
class PaymentListView(PermissionRequiredMixin, ListView):
    permission_required = 'finance.view_payment'
    model = Payment
    context_object_name = 'payments'
    

class PaymentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'finance.view_payment'
    model = Payment
    context_object_name = 'payment'

class PaymentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'finance.add_payment'
    model = Payment
    form_class = CustomPaymentForm

class PaymentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'finance.change_payment'
    model = Payment
    form_class = CustomPaymentForm

class PaymentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'finance.delete_payment'
    model = Payment
    success_url = reverse_lazy('payment_list')

class ServiceListView(PermissionRequiredMixin, ListView):
    permission_required = 'finance.view_service'
    model = Service
    context_object_name = 'service'

class ServiceDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'finance.view_service'
    model = Service
    context_object_name = 'service'

class ServiceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'finance.add_service'
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

class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'finance.change_service'
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

class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'finance.delete_service'
    model = Service
    success_url = reverse_lazy('service_list')

@login_required(login_url='login')
@permission_required('finance.view_payment')
def service_payments_view(request, pk):
    payments = Payment.objects.filter(service=pk)
    context = {'payments': payments}
    return render(request, 'finance/payment_list.html', context)
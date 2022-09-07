from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
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
        form = super(ServiceCreateView, self).get_form(form_class=form_class)
        for key in form.fields:
            form.fields[key].widget.attrs.update({'class': 'laptop-form-fields'})
        return form

class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'

class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('service_list')

def service_payments_view(request, pk):
    payments = Payment.objects.filter(service=pk)
    context = {'payments': payments}
    return render(request, 'finance/payment_list.html', context)
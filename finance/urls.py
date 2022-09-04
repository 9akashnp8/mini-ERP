from django.urls import path

from . import views

urlpatterns = [
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment_add'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('payments/<int:pk>/edit', views.PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<int:pk>/delete', views.PaymentDeleteView.as_view(), name='payment_delete'),

    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_add'),
    path('services/<int:pk>/edit', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete', views.ServiceDeleteView.as_view(), name='service_delete'),
    
    path('services/<int:pk>/payments/', views.service_payments_view, name='service_payments'),

    path('ajax/get-payment-amount/', views.get_payment_amount, name='get_payment_amount'),
]
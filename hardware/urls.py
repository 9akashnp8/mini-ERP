from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('onboarding/', views.onboading),
    path('replace/', views.replace),
    path('return/', views.exit_return),
    path('dash_employees/', views.employees, name='dash_employees'),
    path('employee/<str:pk>', views.employee, name='employee'),
    path('employee_add/', views.employee_add, name='employee_add'),
    path('employee_edit/<str:pk>', views.employee_edit, name='employee_edit'),
    path('employee_del/<str:pk>', views.employee_del, name='employee_del'),
]

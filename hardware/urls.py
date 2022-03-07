from django.urls import path
from . import views

urlpatterns = [
    #Main
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('', views.home, name='home'),
    path('onboarding/', views.onboading),
    path('replace/', views.replace),
    path('return/', views.exit_return),

    #Employees
    path('dash_employees/', views.employees, name='dash_employees'),
    path('employee/<str:pk>', views.employee, name='employee'),
    path('employee_add/', views.employee_add, name='employee_add'),
    path('employee_edit/<str:pk>', views.employee_edit, name='employee_edit'),
    path('employee_del/<str:pk>', views.employee_del, name='employee_del'),
    path('empprofile', views.employeeProfile, name='empprofile'),
    path('empSettingsPage/', views.empSettingsPage, name='empSettingsPage'),

    ##Laptop
    path('dash_laptops/', views.laptops, name='dash_laptops'),
    path('laptop/<str:pk>', views.laptop, name='laptop'),
    path('laptop_add/', views.laptop_add, name='laptop_add'),
    path('laptop_edit/<str:pk>', views.laptop_edit, name='laptop_edit'),
    path('laptop_del/<str:pk>', views.laptop_del, name='laptop_del'),
    path('lap_image_history/<str:pk>', views.lap_image_history, name='lap_image_history'),

    #Onboarding
    path('onbrd_emp_add', views.onbrd_emp_add, name='onbrd_emp_add'),
    path('onbrd_hw_assign', views.onbrd_hw_assign, name='onbrd_hw_assign'),
    path('onbrd_complete/<str:pk>', views.onbrd_complete, name='onbrd_complete'),

    #Exit
    path('emp_exit/', views.emp_exit, name='emp_exit'),
    path('emp_exit_confirm/<str:pk>', views.emp_exit_confirm, name='emp_exit_confirm'),
    path('emp_exit_complete/<str:pk>', views.emp_exit_complete, name='emp_exit_complete'),

]

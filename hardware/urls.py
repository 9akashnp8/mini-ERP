from django.urls import path
from . import views

urlpatterns = [
    #Main
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('', views.home, name='home'),
    path('onboarding/', views.onboading),
    path('replace/', views.replace, name='replace'),
    path('replace_confirm/<str:pk>', views.replace_confirm, name='replace_confirm'),
    path('replace_assign_new/<str:pk>', views.replace_assign_new, name='replace_assign_new'),
    path('replace_complete/<str:pk>', views.replace_complete, name='replace_complete'),

    #Employee URL Paths
    path('employees/', views.employee_list_view, name='dash_employees'),
    path('employee/<str:pk>', views.employee, name='employee'),
    path('employees/add/', views.employee_add_view, name='employee_add'),
    path('employee/<str:pk>/edit/', views.employee_edit_view, name='employee_edit'),
    path('employee/<str:pk>/delete/', views.employee_delete_view, name='employee_del'),
    path('profile/', views.employee_profile_view, name='empprofile'),
    path('profile/edit/', views.employee_profile_edit_view, name='empSettingsPage'),

    #Laptop URL Paths
    path('laptops/', views.laptops_list_view, name='dash_laptops'),
    path('laptop/<str:pk>', views.laptop, name='laptop'),
    path('laptops/add/', views.laptop_add_view, name='laptop_add'),
    path('laptop/<str:pk>/edit/', views.laptop_edit_view, name='laptop_edit'),
    path('laptop/<str:pk>/delete/', views.laptop_delete_view, name='laptop_del'),

    #Onboarding
    path('onbrd_emp_add', views.onbrd_emp_add, name='onbrd_emp_add'),
    path('onbrd_hw_assign', views.onbrd_hw_assign, name='onbrd_hw_assign'),
    path('onbrd_complete/<str:pk>', views.onbrd_complete, name='onbrd_complete'),

    #Exit
    path('emp_exit/', views.emp_exit, name='emp_exit'),
    path('emp_exit_confirm/<str:pk>', views.emp_exit_confirm, name='emp_exit_confirm'),
    path('emp_exit_complete/<str:pk>', views.emp_exit_complete, name='emp_exit_complete'),

    path('ajax/load-designations/', views.load_designations, name='load_designations'),

]

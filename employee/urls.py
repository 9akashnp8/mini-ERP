from django.urls import path
from . import views

urlpatterns = [

    #Onboarding
    path('onboard/add/', views.onboarding_add_employee_view, name='onbrd_emp_add'),
    path('onboard/assign/<str:pk>/', views.onboarding_assign_hardware_view, name='onbrd_hw_assign'),
    path('onboard/complete/<str:pk>/', views.onboarding_complete_view, name='onbrd_complete'),

    #Exit
    path('exit/', views.emp_exit, name='emp_exit'),
    path('exit_confirm/<str:pk>', views.emp_exit_confirm, name='emp_exit_confirm'),
    path('exit_complete/<str:pk>', views.emp_exit_complete, name='emp_exit_complete'),

    #Main
    path('', views.employee_list_view, name='dash_employees'),
    path('add/', views.employee_add_view, name='employee_add'),
    path('<str:pk>/', views.employee, name='employee'),
    path('<str:pk>/edit/', views.employee_edit_view, name='employee_edit'),
    path('<str:pk>/delete/', views.employee_delete_view, name='employee_del'),
    path('profile/', views.employee_profile_view, name='empprofile'),
    path('profile/edit/', views.employee_profile_edit_view, name='empSettingsPage'),

    #Misc
    path('htmx/load-designations/', views.load_designations, name='load_designations'),
]


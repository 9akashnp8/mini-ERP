from django.urls import path
from . import views

urlpatterns = [

    #Laptop URL Paths
    path('laptops/', views.laptops_list_view, name='dash_laptops'),
    path('laptop/add/', views.laptop_add_view, name='laptop_add'),
    path('laptop/<str:pk>/', views.laptop, name='laptop'),
    path('laptop/<str:pk>/edit/', views.laptop_edit_view, name='laptop_edit'),
    path('laptop/<str:pk>/delete/', views.laptop_delete_view, name='laptop_del'),
    path('laptop-return/<str:pk>/', views.laptop_return, name='replace_confirm'),
    path('laptop/<str:pk>/form/', views.generate_hardware_form, name='generate_hardware_form'),

    path('htmx/load-buildings/', views.load_buildings, name='load_buildings'),
    path('htmx/search-result-assign/', views.search_results_for_laptop_assignment, name='search_results_for_laptop_assignment'),
    path('htmx/search-result-replace/', views.search_results_for_laptop_replacement, name='search_results_for_laptop_replacement'),
    path('htmx/search-result-return/', views.search_results_for_laptop_return, name='search_results_for_laptop_return'),

]

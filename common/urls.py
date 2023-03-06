from django.urls import path

from . import views
from employee import views as employee_views
from hardware import views as hardware_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path(
        'admin-panel/department/',
        employee_views.DepartmentListCreateView.as_view(), 
        name='department_list_create'
    ),
    path(
        'admin-panel/designation/',
        employee_views.DesignationListCreateView.as_view(),
        name='designation_list_create'),
    path(
        'admin-panel/location/',
        employee_views.LocationListCreateView.as_view(),
        name='location_list_create'
    ),
    path(
        'admin-panel/building/',
        hardware_views.BuildingListCreateView.as_view(),
        name='building_list_create'
    ),
    path(
        'admin-panel/brands/',
        hardware_views.BrandListCreateView.as_view(),
        name='brand_list_create'
    ),
]
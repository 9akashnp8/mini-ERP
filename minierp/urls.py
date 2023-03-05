"""minierp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from employee.views import DepartmentListCreateView, DesignationListCreateView, LocationListCreateView

urlpatterns = [
    path('admin/', admin.site.urls),

    #General Views
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/department/', DepartmentListCreateView.as_view(), name='department_list_create'),
    path('admin-panel/designation/', DesignationListCreateView.as_view(), name='designation_list_create'),
    path('admin-panel/location/', LocationListCreateView.as_view(), name='location_list_create'),
    path('', views.home, name='home'),

    #App Views
    path('employee/', include('employee.urls')),
    path('hardware/', include('hardware.urls')),
    path('finance/', include('finance.urls')),
    path('api/', include('api.urls')),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
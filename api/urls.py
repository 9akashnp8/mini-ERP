from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# Employee routes
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'department', DepartmentViewSet, basename='department')
router.register(r'designation', DesignationViewSet, basename='designation')
router.register(r'location', LocationViewSet, basename='location')

#Hardware routes
router.register(r'laptop', LaptopViewSet, basename='laptop')
router.register(r'laptop-brand', LaptopBrandViewSet, basename='laptop-brand')
router.register(r'building', BuildingViewSet, basename='building')


urlpatterns = [
    path('', include(router.urls))
]
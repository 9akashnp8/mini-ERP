from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    employee,
    hardware,
    finance
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# Employee routes
router.register(r'employee',  employee.EmployeeViewSet, basename='employee')
router.register(r'department', employee.DepartmentViewSet, basename='department')
router.register(r'designation', employee.DesignationViewSet, basename='designation')
router.register(r'location', employee.LocationViewSet, basename='location')

# Hardware routes
router.register(r'laptop', hardware.LaptopViewSet, basename='laptop')
router.register(r'laptop-brand', hardware.LaptopBrandViewSet, basename='laptop-brand')
router.register(r'building', hardware.BuildingViewSet, basename='building')

# Hardware Chart URLs
hardware_chart_urls = [
    path('laptop/chart/general/', hardware.LaptopChartAPI.as_view(), name='general_laptop_chart_url')
]

# Finance routes
router.register(r'payment', finance.PaymentViewSet, basename='payment')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + hardware_chart_urls
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView

from .authentication import CookieTokenObtainPairView, CookieTokenRefreshView
from .views.hardware import laptop
from .views import (
    employee,
    finance,
    common,
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# Employee routes
router.register(
    r'employee',
    employee.EmployeeViewSet,
    basename='employee'
)
router.register(
    r'department',
    employee.DepartmentViewSet,
    basename='department'
)
router.register(
    r'designation',
    employee.DesignationViewSet,
    basename='designation'
)
router.register(
    r'location',
    employee.LocationViewSet,
    basename='location'
)
employee_urls = [
    path(
        'employee/<str:id>/history/',
        employee.EmployeeHistoryAPIView.as_view(),
        name='employee_histoy_api'
    ),
    path(
        'employee/<str:id>/laptops/',
        employee.EmployeeLaptopListView.as_view(),
        name="employee_laptop_list"
    ),
    path(
        'user/',
        employee.UserCreateView.as_view(),
        name="user_list_create_api"
    ),
    path(
        'employee-app-settings/',
        common.EmployeeAppSettingsAPI.as_view(),
        name="employee_app_settings"
    ),
]

# Hardware routes
router.register(
    r'laptop',
    laptop.LaptopViewSet,
    basename='laptop'
)
router.register(
    r'laptop-brand',
    laptop.LaptopBrandViewSet,
    basename='laptop-brand'
)
router.register(
    r'building',
    laptop.BuildingViewSet,
    basename='building'
)
hardware_urls = [
    path(
        'laptop/<str:id>/history/',
        laptop.LaptopHistoryAPIView.as_view(),
        name='laptop_history_api',
    ),
    path(
        'laptop-screen-types/',
        laptop.LaptopScreenTypeAPI.as_view(),
        name='laptop_screen_types',
    ),
    path(
        'laptop-statuses/',
        laptop.LaptopStatusAPI.as_view(),
        name='laptop_status',
    ),
    path(
        'laptop-owner-types/',
        laptop.LaptopOwnerAPI.as_view(),
        name='laptop_owner_types',
    ),
    path(
        'hardware-app-settings/',
        common.HardwareAppSettingsAPI.as_view(),
        name="hardware_app_settings"
    ),
]

# Hardware Chart URLs
hardware_chart_urls = [
    path(
        'laptop/chart/general/',
        laptop.LaptopChartAPI.as_view(),
        name='general_laptop_chart_url'
    )
]

# Finance routes
router.register(
    r'payment',
    finance.PaymentViewSet,
    basename='payment'
)


urlpatterns = [
    path('', include(router.urls)),
    path(
        'token/',
        CookieTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        CookieTokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
] + hardware_chart_urls + employee_urls + hardware_urls

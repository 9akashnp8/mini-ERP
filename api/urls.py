from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import EmployeeViewSet

router = DefaultRouter()
router.register(r'employee', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls))
]
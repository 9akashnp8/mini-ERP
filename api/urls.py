from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *
urlpatterns = [
    #Auth paths
    path('auth/', obtain_auth_token),

    #Employee Paths
    path('employee/<int:pk>/', GetEmployeeDetailAPIView.as_view(), name='GetEmployeeDetailAPIView'),
    path('employee/', ListOrCreateEmployeeAPIView.as_view(), name='ListOrCreateEmployeeAPIView'),
    path('employee/<int:pk>/update/', UpdateEmployeeAPIView.as_view(), name='UpdateEmployeeAPIView'),
    path('employee/<int:pk>/delete/', DestroyEmployeeAPIView.as_view(), name='DestroyEmployeeAPIView')
]
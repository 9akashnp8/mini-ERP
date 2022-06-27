from django.urls import path

from .views import *
urlpatterns = [
    #Employee Paths
    path('employee/<int:pk>/', GetEmployeeDetailAPIView.as_view(), name='GetEmployeeDetailAPIView'),
    path('employee/', ListOrCreateEmployeeAPIView.as_view(), name='ListOrCreateEmployeeAPIView'),
    path('employee/<int:pk>/update/', UpdateEmployeeAPIView.as_view(), name='UpdateEmployeeAPIView'),
    path('employee/<int:pk>/delete/', DestroyEmployeeAPIView.as_view(), name='DestroyEmployeeAPIView')
]
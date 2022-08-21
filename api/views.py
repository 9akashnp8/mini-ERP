from rest_framework import viewsets

from employee.models import Employee
from employee.serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# class GetEmployeeDetailAPIView(generics.RetrieveAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = 'pk'

# class ListOrCreateEmployeeAPIView(generics.ListCreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

#     def perform_create(self, serializer):
#         serializer.save()

# class UpdateEmployeeAPIView(generics.UpdateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = 'pk'

#     def perform_update(self, serializer):
#         serializer.save()

# class DestroyEmployeeAPIView(generics.DestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = 'pk'

#     def perform_destroy(self, instance):
#         super().perform_destroy(instance)

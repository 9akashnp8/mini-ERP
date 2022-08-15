from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import *


#Resources for Import-Export library
class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        import_id_fields = ('emp_id',)

class DesignationResource(resources.ModelResource):
    class Meta:
        model = Designation
        exclude = ('id')
        import_id_fields = ('designation_id',)

#Import Export classes for Admin page integration
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource

class DesignationModelAdmin(ImportExportModelAdmin):
    resource_class = DesignationResource

#Registering Models
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Designation, DesignationModelAdmin)
admin.site.register(Location)
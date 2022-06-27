from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import *

class LaptopResource(resources.ModelResource):
    class Meta:
        model = Laptop

class EmployeeResource(resources.ModelResource):
    
    class Meta:
        model = Employee
        import_id_fields = ('emp_id',)

class HardwareAdmin(ImportExportModelAdmin):
    list_display = ('id', 'hardware_id', 'emp_id')

class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource

class LaptopModelAdmin(ImportExportModelAdmin):
    resource_class = LaptopResource


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Location)
admin.site.register(Hardware, HardwareAdmin)
admin.site.register(LaptopBrand)
admin.site.register(LaptopModel)
admin.site.register(LaptopMedia)
admin.site.register(Laptop, LaptopModelAdmin)




# Register your models here.

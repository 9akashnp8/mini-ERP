from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import *

class HardwareAdmin(ImportExportModelAdmin):
    list_display = ('id', 'hardware_id', 'emp_id')
    pass

class EmployeeAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Location)
admin.site.register(Hardware, HardwareAdmin)
admin.site.register(LaptopBrand)
admin.site.register(LaptopModel)
admin.site.register(LaptopMedia)
admin.site.register(Laptop, SimpleHistoryAdmin)




# Register your models here.

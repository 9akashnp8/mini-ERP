from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from hardware.models import *

#Resources for Import-Export library
class LaptopResource(resources.ModelResource):
    class Meta:
        model = Laptop

#Import Export classes for Admin page integration
class HardwareAdmin(ImportExportModelAdmin):
    list_display = ('id', 'hardware_id', 'emp_id')

class LaptopModelAdmin(ImportExportModelAdmin):
    resource_class = LaptopResource

#Register models
admin.site.register(Building)
admin.site.register(Hardware, HardwareAdmin)
admin.site.register(LaptopBrand)
admin.site.register(LaptopModel)
admin.site.register(Laptop, LaptopModelAdmin)
admin.site.register(HardwareAppSetting)
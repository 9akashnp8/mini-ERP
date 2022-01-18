from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *

class HardwareAdmin(admin.ModelAdmin):
    list_display = ('id', 'hardware_id', 'emp_id')

admin.site.register(Employee, SimpleHistoryAdmin)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Hardware, HardwareAdmin)
admin.site.register(LaptopBrand)
admin.site.register(LaptopModel)
admin.site.register(LaptopMedia)
admin.site.register(Laptop)




# Register your models here.

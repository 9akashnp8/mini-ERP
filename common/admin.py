from django.contrib import admin

from .models import (
    EmployeeAppSetting,
    HardwareAppSetting
)

# Register your models here.
admin.site.register(EmployeeAppSetting)
admin.site.register(HardwareAppSetting)
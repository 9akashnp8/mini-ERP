from django.contrib import admin
from import_export import resources
from hardware.models import (
    Laptop,
    LaptopV2,
    Building,
    Hardware,
    HardwareType,
    HardwareOwner,
    HardwareCondition,
    LaptopBrand,
    LaptopOwner,
    LaptopScreenSize,
    HardwareAppSetting,
    HardwareAssignment,
)


# Resources for Import-Export library
class LaptopResource(resources.ModelResource):
    class Meta:
        model = Laptop


# Register models
admin.site.register(Hardware)
admin.site.register(HardwareType)
admin.site.register(HardwareOwner)
admin.site.register(HardwareCondition)
admin.site.register(HardwareAppSetting)
admin.site.register(HardwareAssignment)
admin.site.register(LaptopBrand)
admin.site.register(LaptopV2)
admin.site.register(LaptopOwner)
admin.site.register(LaptopScreenSize)
admin.site.register(Building)

from django.contrib import admin
from .models import *

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Location)
admin.site.register(User)

# Register your models here.

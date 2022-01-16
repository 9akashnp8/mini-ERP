from csv import list_dialects
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *

admin.site.register(Employee, SimpleHistoryAdmin)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Location)
admin.site.register(User)




# Register your models here.

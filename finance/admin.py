from django.contrib import admin

from .models import *

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'service')

# Register your models here.
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Service)
admin.site.register(Platform)
admin.site.register(Category)
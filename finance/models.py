from django.db import models
from django.urls import reverse

from employee.models import Department

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Platform(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    platform = models.CharField(max_length=100)

    def __str__(self):
        return self.platform

class Service(models.Model):
    INTERVAL_CHOICES = (
        ('OT', 'One Time'),
        ('M', 'Monthly'),
        ('Q', 'Quaterly'),
        ('H', 'Half-Yearly'),
        ('Y', 'Yearly')
    )
    service_id = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    platform = models.ForeignKey(Platform, null=True, on_delete=models.SET_NULL)
    end_user = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    payment_interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES)
    current_cost = models.CharField(max_length=50)
    estimated_due_date = models.IntegerField()
    status = models.CharField(max_length=10, choices=(('Active', 'Active'), ('Inactive', 'Inactive')))

    def __str__(self):
        return self.platform.platform
    
    def get_absolute_url(self):
        return reverse('service_detail', args=[str(self.id)])

class Payment(models.Model):
    PAYMENT_MODES = (
        ('Card', 'Card'),
        ('Paypal', 'Paypal')
    )

    PAYMENT_STATUSES = (
        ('Paid', 'Paid'),
        ('Pending', 'Pending')
    )

    payment_id = models.CharField(max_length=100, blank=True)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    payment_for_month = models.DateField()
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUSES, default="Pending")
    amount = models.CharField(max_length=50, null=True, blank=True)
    invoice_no = models.CharField(max_length=150, null=True, blank=True)
    invoice_doc = models.FileField(null=True, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES, null=True, blank=True)
    card_no = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.payment_id)

    def get_absolute_url(self):
        return reverse('payment_detail', args=[str(self.id)])
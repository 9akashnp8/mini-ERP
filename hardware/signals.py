from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Employee, Hardware, Laptop

def createEmployee(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='employee')
        instance.groups.add(group)
        Employee.objects.create(
            user=instance,
            emp_email = instance.email,
        )

post_save.connect(createEmployee, sender=User)

'''
def autoIncrementingHardwareID(sender, instance, created, **kwargs):
    if created:
        if not instance.hardware_id:
            prefix = 'LAK-LAP'
            id = Laptop.objects.count()+1
            instance.hardware_id = prefix+'-'+'{0:04d}'.format(id)

post_save.connect(autoIncrementingHardwareID, sender=Laptop)
'''
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.forms import ValidationError
from .models import Employee

def createUser(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='employee')
        User.objects.create_user(username=instance.emp_email, email=instance.emp_email, password='lakshya123',).groups.add(group)
        #User.objects.get(username=instance.emp_email)
        usercreated = User.objects.get(username=instance.emp_email)
        instance.user = User.objects.get(username=instance.emp_email)
        instance.save()

post_save.connect(createUser, sender=Employee)

'''
def autoIncrementingHardwareID(sender, instance, created, **kwargs):
    if created:
        if not instance.hardware_id:
            prefix = 'LAK-LAP'
            id = Laptop.objects.count()+1
            instance.hardware_id = prefix+'-'+'{0:04d}'.format(id)

post_save.connect(autoIncrementingHardwareID, sender=Laptop)
'''
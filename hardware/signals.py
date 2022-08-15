from django.db.models.signals import post_save
from hardware.models import Laptop

def createHardwareID(sender, instance, created, **kwargs):
    
    if created:
        if not instance.hardware_id:
            instance.hardware_id = "LAK-LAP-{0:04d}".format(instance.id)
            instance.save()
        
post_save.connect(createHardwareID, sender=Laptop)
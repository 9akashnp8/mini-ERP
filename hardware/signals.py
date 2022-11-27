from django.db.models.signals import post_save
from django.db.utils import OperationalError
from hardware.models import Laptop, HardwareAppSettings

try:
    hardware_id_prefix = HardwareAppSettings.objects.get(id=1).laptop_hardware_id_prefix
except (OperationalError, HardwareAppSettings.DoesNotExist):
    hardware_id_prefix = "LAPTOP"

def createHardwareID(sender, instance, created, **kwargs):
    
    if created:
        if not instance.hardware_id:
            instance.hardware_id = hardware_id_prefix + "-{0:04d}".format(instance.id)
            instance.save()
        
post_save.connect(createHardwareID, sender=Laptop)
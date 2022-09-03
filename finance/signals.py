from django.db.models.signals import post_save
from finance.models import Payment, Service

def createPaymentID(sender, instance, created, **kwargs):
    
    if created:
        if not instance.payment_id:
            instance.payment_id = "LAK-FIN/PAY-{0:04d}".format(instance.id)
            instance.save()
        
post_save.connect(createPaymentID, sender=Payment)

def createServiceID(sender, instance, created, **kwargs):
    
    if created:
        if not instance.service_id:
            instance.service_id = "LAK-FIN/SER-{0:02d}".format(instance.id)
            instance.save()
        
post_save.connect(createServiceID, sender=Service)
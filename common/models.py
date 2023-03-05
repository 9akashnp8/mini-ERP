from django.db import models

# Create your models here.
class BaseSetting(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        skip deletion as to retain the
        only required object
        """
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class EmployeeAppSetting(BaseSetting):
    emp_id_prefix = models.CharField(max_length=200)

class HardwareAppSetting(BaseSetting):
    hardware_id_prefix = models.CharField(max_length=200)
    default_processor = models.CharField(max_length=30)
    default_ram = models.CharField(max_length=10)
    default_storage = models.CharField(max_length=10)
    screen_sizes = models.CharField(max_length=100)
    rental_vendors = models.CharField(max_length=500)
    organization_name = models.CharField(max_length=100)
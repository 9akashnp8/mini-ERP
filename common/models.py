from django.db import models
from django.core.cache import cache
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class BaseSetting(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        """
        skip deletion as to retain the
        only required object
        """
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

class EmployeeAppSetting(BaseSetting):
    emp_id_prefix = models.CharField(
        max_length=255,
        default='MYORG'
    )

    def __str__(self) -> str:
        return 'Employee App Setting'

class HardwareAppSetting(BaseSetting):
    hardware_id_prefix = models.CharField(
        max_length=255,
        default='LAP'
    )
    default_processor = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    default_ram = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    default_storage = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    screen_sizes = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    screen_sizes = ArrayField(
        base_field=models.CharField(max_length=255),
        default=['14 inch, 15 inch']
    )
    rental_vendors = ArrayField(
        base_field=models.CharField(max_length=255),
        blank=True,
        null=True
    )
    organization_name = models.CharField(
        max_length=255,
        default='My Organization'
    )

    def __str__(self) -> str:
        return 'Hardware App Setting'
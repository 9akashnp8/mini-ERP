from import_export import resources
from .models import Hardware

class HardwareResource(resources.ModelResource):
    class Meta:
        model = Hardware
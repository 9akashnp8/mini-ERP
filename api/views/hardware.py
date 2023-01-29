from rest_framework import viewsets

from hardware.models import (
    Laptop,
    LaptopBrand,
    Building
)
from api.serializers import (
    LaptopSerializer,
    LaptopBrandSerializer,
    BuildingSerializer
)

class LaptopViewSet(viewsets.ModelViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer

class LaptopBrandViewSet(viewsets.ModelViewSet):
    queryset = LaptopBrand.objects.all()
    serializer_class = LaptopBrandSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
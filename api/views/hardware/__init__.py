from rest_framework.viewsets import ModelViewSet

from api.serializers.hardware import HardwareTypeSerializer

from hardware.models import HardwareType


class HardwareTypeViewSet(ModelViewSet):
    serializer_class = HardwareTypeSerializer
    queryset = HardwareType.objects.all()

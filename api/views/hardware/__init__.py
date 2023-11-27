from rest_framework.viewsets import ModelViewSet

from api.serializers.hardware import (
    HardwareTypeSerializer,
    HardwareOwnerSerializer,
    HardwareConditionSerializer,
)

from hardware.models import (
    HardwareType,
    HardwareOwner,
    HardwareCondition,
)


class HardwareTypeViewSet(ModelViewSet):
    serializer_class = HardwareTypeSerializer
    queryset = HardwareType.objects.all()


class HardwareOwnerViewSet(ModelViewSet):
    serializer_class = HardwareOwnerSerializer
    queryset = HardwareOwner.objects.all()


class HardwareConditionViewSet(ModelViewSet):
    serializer_class = HardwareConditionSerializer
    queryset = HardwareCondition.objects.all()

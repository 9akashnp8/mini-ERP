from rest_framework.viewsets import ModelViewSet

from api.serializers.hardware import (
    HardwareListRetrieveSerializer,
    HardwareCreateUpdateDestroySerializer,
    HardwareTypeSerializer,
    HardwareOwnerSerializer,
    HardwareConditionSerializer,
)

from hardware.models import (
    Hardware,
    HardwareType,
    HardwareOwner,
    HardwareCondition,
)


class HardwareViewSet(ModelViewSet):
    serializer_class = HardwareCreateUpdateDestroySerializer
    queryset = Hardware.objects.all()
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return HardwareListRetrieveSerializer
        return HardwareCreateUpdateDestroySerializer


class HardwareTypeViewSet(ModelViewSet):
    serializer_class = HardwareTypeSerializer
    queryset = HardwareType.objects.all()


class HardwareOwnerViewSet(ModelViewSet):
    serializer_class = HardwareOwnerSerializer
    queryset = HardwareOwner.objects.all()


class HardwareConditionViewSet(ModelViewSet):
    serializer_class = HardwareConditionSerializer
    queryset = HardwareCondition.objects.all()

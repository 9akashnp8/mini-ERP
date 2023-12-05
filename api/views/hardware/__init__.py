from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django_filters import rest_framework as filters

from api.serializers.hardware import (
    HardwareListRetrieveSerializer,
    HardwareCreateUpdateDestroySerializer,
    HardwareTypeSerializer,
    HardwareOwnerSerializer,
    HardwareConditionSerializer,
    HardwareAssignmentSerializer,
    HardwareAssignmentCreateSerializer,
    HardwareAssignmentUpdateSerializer,
)
from api.filters import HardwareAssignmentFilter

from hardware.models import (
    Hardware,
    HardwareType,
    HardwareOwner,
    HardwareCondition,
    HardwareAssignment,
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


class HardwareAssignmentViewSet(ModelViewSet):
    queryset = HardwareAssignment.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = HardwareAssignmentFilter

    def get_serializer_class(self):
        if self.action == "create":
            return HardwareAssignmentCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return HardwareAssignmentUpdateSerializer
        return HardwareAssignmentSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({"status": "fail", "message": "Not Allowed"}, status=405)

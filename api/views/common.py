from rest_framework.generics import RetrieveUpdateAPIView

from common.models import (
    EmployeeAppSetting,
    HardwareAppSetting,
)
from api.serializers import (
    EmployeeAppSettingsSerializer,
    HardwareAppSettingsSerializer,
)

class EmployeeAppSettingsAPI(RetrieveUpdateAPIView):
    serializer_class = EmployeeAppSettingsSerializer

    def get_object(self):
        return EmployeeAppSetting.load()

class HardwareAppSettingsAPI(RetrieveUpdateAPIView):
    serializer_class = HardwareAppSettingsSerializer

    def get_object(self):
        return HardwareAppSetting.load()

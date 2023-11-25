from rest_framework import viewsets

from finance.models import Payment
from api.serializers.finance import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

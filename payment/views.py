from payment.models import Payment
from payment.serializers import PaymentSerializer
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('course', 'lesson', 'pay_type')
    ordering_fields = ('data_pay', )
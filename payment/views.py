from main.models import Course

from payment.models import Payment
from payment.serializers import PaymentSerializer
from payment.services import stripe_payment_create

from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    permission_classes = [IsAuthenticated]

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('course', 'lesson', 'pay_type')
    ordering_fields = ('data_pay', )


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data

        if data['pay_type'] == Payment.PAY_CARD:

            try:
                response_payment = stripe_payment_create(data['amount'], Course.objects.get(pk=data['course']).title)

                data['user'] = request.user.pk
                data['stripe_url'] = response_payment['url']
                data['stripe_id'] = response_payment['id']
                data['stripe_status'] = response_payment['status']
                data['is_paid'] = False

                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'Оплата возможна только по карте!'}, status=status.HTTP_409_CONFLICT)

from payment.apps import PaymentConfig

from django.urls import path

from payment.views import (PaymentListAPIView)

app_name = PaymentConfig.name

urlpatterns = [
    path('payment/list/', PaymentListAPIView.as_view(), name='payment_list'),
]

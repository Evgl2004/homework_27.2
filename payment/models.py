from django.db import models
from datetime import datetime
from main.models import Course, Lesson
from django.conf import settings

NULLABLE = {'null': True, 'blank': True}


class Payment(models.Model):

    PAY_CARD = 'card'
    PAY_CASH = 'cash'

    PAY_TYPES = (
        (PAY_CARD, 'перевод'),
        (PAY_CASH, 'наличные'),
    )

    data_pay = models.DateTimeField(default=datetime.now, verbose_name='дата оплаты')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='урок')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='сумма')
    pay_type = models.CharField(max_length=4, default=PAY_CARD, choices=PAY_TYPES, verbose_name='способ оплаты')

    stripe_id = models.CharField(max_length=255, **NULLABLE, verbose_name='идентификатор оплаты')
    stripe_status = models.CharField(max_length=10, **NULLABLE, verbose_name='статус оплаты')
    stripe_url = models.CharField(max_length=500, **NULLABLE, verbose_name='ссылка оплаты')

    is_paid = models.BooleanField(default=False, verbose_name='оплачено')

    def __str__(self):
        return f'{self.title}'

    def __str__(self):
        if self.course:
            return f'{self.course} - {self.pay_type} - {self.amount}'
        elif self.lesson:
            return f'{self.lesson} - {self.pay_type} - {self.amount}'
        else:
            return f'{self.course} - {self.lesson} - {self.pay_type} - {self.amount}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

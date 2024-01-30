from celery import shared_task

from main.models import Course, SubscriptionsUserOnCourse

from django.core.mail import send_mail
from django.conf import settings

from smtplib import SMTPException


@shared_task
def task_send_mail(pk_course):
    select_subscriptions = SubscriptionsUserOnCourse.objects.filter(is_active=True, course=pk_course)

    if select_subscriptions.exists():
        for instance in select_subscriptions:
            try:
                result = send_mail(
                    subject=f'Курс {Course.objects.filter(pk=pk_course).first().title}',
                    message='Произошло обновление курса на который вы подписаны',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[instance.user.email],
                    fail_silently=False
                )

                print(result)

            except SMTPException as error:
                print(error)

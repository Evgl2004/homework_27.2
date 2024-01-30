from datetime import datetime, timedelta

from celery import shared_task

from users.models import User


@shared_task
def deactivation_user_last_login():
    for user in User.objects.filter(is_active=True):
        if (not user.last_login is None and
                datetime.now() >= (user.last_login + timedelta(days=30)).replace(tzinfo=None)):
            user.is_active = False
            user.save()
            print(f'{user} | id = {user.id} | заблокирован')

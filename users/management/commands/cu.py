from django.core.management import BaseCommand
from users.models import User


class Command (BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='pytest22@test.ru',
            first_name='Иван',
            last_name='Петров',
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        user.set_password('1234')
        user.save()

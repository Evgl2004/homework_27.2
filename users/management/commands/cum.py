from django.core.management import BaseCommand
from users.models import User


class Command (BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='pytest24@test.ru',
            first_name='Александр',
            last_name='Сидоров',
            is_staff=True,
            is_superuser=False,
            is_active=True
        )

        user.set_password('1234')
        user.save()

from django.core.management import BaseCommand
from main.models import Course, Lesson
from payment.models import Payment
from users.models import User
from datetime import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):

        user_test = User.objects.get(id=2)

        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Payment.objects.all().delete()

        course_list_che = [
            {'title': 'Химия', 'description': 'Лучший курс химии'},
        ]

        course_list_bio = [
            {'title': 'Биология', 'description': 'Лучший курс биологии'},
        ]

        lesson_list_che = [
            {'title': 'Урок №01', 'description': 'Техника безопасности', 'course': 1},
            {'title': 'Урок №02', 'description': 'Таблица Менделеева', 'course': 1},
        ]

        lesson_list_bio = [
            {'title': 'Урок #01', 'description': 'Введение в биологию', 'course': 2},
            {'title': 'Урок #02', 'description': 'Теория Дарвина', 'course': 2},
        ]

        pay_course_che = [
            {
                'data_pay': datetime(2023, 11, 14, 12, 30),
                'user':  user_test,
                'course': 1,
                'amount': 45000,
                'pay_type': Payment.PAY_CARD
            },
        ]

        pay_course_bio = [
            {
                'data_pay': datetime(2023, 12, 16, 11, 33),
                'user': user_test,
                'course': 2,
                'amount': 55000,
                'pay_type': Payment.PAY_CARD
            },
        ]

        pay_lesson_che = [
            {
                'data_pay': datetime(2023, 11, 16, 15, 12),
                'user': user_test,
                'lesson': 1,
                'amount': 5000,
                'pay_type': Payment.PAY_CARD
            },
        ]

        pay_lesson_bio = [
            {
                'data_pay': datetime(2023, 12, 23, 20, 5),
                'user': user_test,
                'lesson': 3,
                'amount': 2500,
                'pay_type': Payment.PAY_CASH
            },
        ]

        for course_che_item in course_list_che:
            course_che_obj = Course.objects.create(**course_che_item)

            for lesson_che_item in lesson_list_che:
                lesson_che_item['course'] = course_che_obj
                lesson_che_obj = Lesson.objects.create(**lesson_che_item)

                for pay_lesson_che_item in pay_lesson_che:
                    pay_lesson_che_item['lesson'] = lesson_che_obj
                    Payment.objects.create(**pay_lesson_che_item)

            for pay_course_che_item in pay_course_che:
                pay_course_che_item['course'] = course_che_obj
                Payment.objects.create(**pay_course_che_item)

        for course_bio_item in course_list_bio:
            course_bio_obj = Course.objects.create(**course_bio_item)

            for lesson_bio_item in lesson_list_bio:
                lesson_bio_item['course'] = course_bio_obj
                lesson_bio_obj = Lesson.objects.create(**lesson_bio_item)

                for pay_lesson_bio_item in pay_lesson_bio:
                    pay_lesson_bio_item['lesson'] = lesson_bio_obj
                    Payment.objects.create(**pay_lesson_bio_item)

            for pay_course_bio_item in pay_course_bio:
                pay_course_bio_item['course'] = course_bio_obj
                Payment.objects.create(**pay_course_bio_item)

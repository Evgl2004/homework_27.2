from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from main.models import Course, Lesson, SubscriptionsUserOnCourse
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', password='test')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Это тестовое описание тестового курса!',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='Тестовая урок',
            description='Это тестовое описание тестового урока!',
            link_to_video='https://www.youtube.com/watch?v=GlLPNVbFU1s',
            owner=self.user,
            course=self.course,
        )

    def test_create_lesson_error(self):
        data_lesson = {
            'title': 'Тестовая урок',
            'description': 'Это тестовое описание тестового урока!',
            'course': self.course.pk
        }

        response = self.client.post(
            '/lesson/create/',
            data=data_lesson
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'link_to_video': ['Обязательное поле.']}
        )

    def test_create_lesson(self):
        data_lesson = {
            'title': 'Тестовая урок',
            'description': 'Это тестовое описание тестового урока!',
            'link_to_video': 'https://www.youtube.com/watch?v=GlLPNVbFU1s',
            'course': self.course.pk
        }

        response = self.client.post(
            '/lesson/create/',
            data=data_lesson
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': self.lesson.id + 1, 'link_to_video': 'https://www.youtube.com/watch?v=GlLPNVbFU1s', 'title': 'Тестовая урок',
             'picture': None, 'description': 'Это тестовое описание тестового урока!',
             'course': self.course.id, 'owner': self.user.id}
        )

    def test_list_lesson(self):
        response = self.client.get(
            '/lesson/list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
             [{'id': self.lesson.id, 'link_to_video': self.lesson.link_to_video,
               'title': self.lesson.title, 'picture': None, 'description': self.lesson.description,
               'course': self.course.id, 'owner': self.user.id}]
        )

    def test_retrieve_lesson(self):
        response = self.client.get(
            f'/lesson/view/{self.lesson.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'link_to_video': self.lesson.link_to_video, 'title': self.lesson.title,
             'picture': None, 'description': self.lesson.description,
             'course': self.course.id, 'owner': self.user.id}
        )

    def test_update_lesson(self):
        data = {
            'title': 'Изменим название для теста!',
        }
        response = self.client.patch(
            f'/lesson/edit/{self.lesson.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'link_to_video': self.lesson.link_to_video,
             'title': 'Изменим название для теста!',
             'picture': None, 'description': self.lesson.description,
             'course': self.course.id, 'owner': self.user.id}
        )

    def test_delete_lesson(self):
        response = self.client.delete(
            f'/lesson/delete/{self.lesson.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Course.objects.all().delete()
        Lesson.objects.all().delete()


class SubscriptionsUserOnCourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', password='test')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Это тестовое описание тестового курса!',
            owner=self.user
        )

        self.subscription_user_on_course = SubscriptionsUserOnCourse.objects.create(
            course=self.course,
            user=self.user,
            is_active=True
        )

        self.course_two = Course.objects.create(
            title='Тестовый курс #2',
            description='Это тестовое описание тестового курса #2!',
            owner=self.user
        )


    def test_create_subscription_user_on_course(self):
        response = self.client.post(
            f'/subscription_user_on_course/create/{self.course_two.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            ['Вы подписались на курс.']
        )

    def test_create_subscription_user_on_course_error(self):
        response = self.client.post(
            f'/subscription_user_on_course/create/{self.course.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT
        )

        self.assertEqual(
            response.json(),
            ['Вы ранее уже подписаны на курс!']
        )

    def test_delete_subscription_user_on_course(self):
        response = self.client.delete(
            f'/subscription_user_on_course/delete/{self.subscription_user_on_course.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def tearDown(self):
        Course.objects.all().delete()
        SubscriptionsUserOnCourse.objects.all().delete()

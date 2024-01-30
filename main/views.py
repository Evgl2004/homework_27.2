from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.serializers import CourseSerializer, LessonSerializer,SubscriptionsUserOnCourseSerializer
from main.models import Course, Lesson, SubscriptionsUserOnCourse
from main.permissions import IsNotModerator, IsObjectOwner, IsObjectOwnerOrModerator, IsSubscriber
from main.paginators import MainPaginator
from main.tasks import task_send_mail

from users.services import is_moderator


class CourseViewSet(viewsets.ModelViewSet):
    """
        Контроллер точки входа набора CRUD для взаимодействия с моделью Курса.
    """

    serializer_class = CourseSerializer
    pagination_class = MainPaginator
    queryset = Course.objects.all()

    # вернул видимость всех курсов, не только своих
    # def get_queryset(self):

        # if is_moderator(self.request.user):
        #     return Course.objects.all()
        #
        # return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer, *args, **kwargs):
        task_send_mail.delay(self.kwargs.get('pk'))
        super().perform_update(serializer)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsObjectOwnerOrModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsObjectOwner]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """
        Контроллер для создания элементов модели Уроки.
    """
    serializer_class = LessonSerializer

    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()
        return super().perform_create(serializer)


class LessonListAPIView(generics.ListAPIView):
    """
        Контроллер для получения списка всех доступных элементов модели Уроки.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MainPaginator

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if is_moderator(self.request.user):
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
        Контроллер для получения детализации элемента модели Уроки.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated, IsObjectOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
        Контроллер для обновления информации элемента модели Уроки.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated, IsObjectOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
        Контроллер для удаления элемента модели Уроки.
    """
    queryset = Lesson.objects.all()

    permission_classes = [IsAuthenticated, IsObjectOwner]


class SubscriptionsUserOnCourseCreateAPIView(generics.CreateAPIView):
    """
        Контроллер для создания элемента модели Подписки - действие 'Подписаться'
    """
    serializer_class = SubscriptionsUserOnCourseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_pk = self.kwargs.get('course_pk')

        if SubscriptionsUserOnCourse.objects.filter(user=request.user.pk, course=course_pk).exists():
            return Response({'Вы ранее уже подписаны на курс!'}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data={'user': request.user.pk, 'course': course_pk, 'is_active': True})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'Вы подписались на курс.'}, status=status.HTTP_201_CREATED)


class SubscriptionsUserOnCourseDeleteAPIView(generics.DestroyAPIView):
    """
        Контроллер для удаления элемента модели Подписки - действие 'Отписаться'.
    """
    queryset = SubscriptionsUserOnCourse.objects.all()
    permission_classes = [IsAuthenticated, IsSubscriber]

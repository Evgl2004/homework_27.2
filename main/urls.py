from main.apps import MainConfig
from rest_framework.routers import DefaultRouter

from django.urls import path

from main.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                        LessonUpdateAPIView, LessonDestroyAPIView)

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/list/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/view/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_view'),
    path('lesson/edit/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_edit'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls

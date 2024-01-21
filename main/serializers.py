from rest_framework import serializers

from main.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lesson(self, instance):
        if instance.lesson.count():
            return instance.lesson.count()
        return 0


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

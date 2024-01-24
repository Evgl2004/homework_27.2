from rest_framework import serializers

from main.models import Course, Lesson
from main.validators import validator_link_video


class LessonSerializer(serializers.ModelSerializer):
    link_to_video = serializers.CharField(validators=[validator_link_video])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lesson(self, instance):
        if instance.lesson.count():
            return instance.lesson.count()
        return 0

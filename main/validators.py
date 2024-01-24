from rest_framework import serializers


def validator_link_video(value):
    if not 'youtube.com' in value:
        raise serializers.ValidationError('Ссылка на видео должна быть только на youtube.com')

from rest_framework import serializers
from .models import Humm
from django.conf import settings


MAX_HUMM_LENGTH = settings.MAX_HUMM_LENGTH


class HummSerializer(serializers.ModelSerializer):
    class Meta:
        model = Humm
        fields = ['content']

    def validated_content(self, value):
        if len(value) > MAX_HUMM_LENGTH:
            raise serializers.ValidationError("This Humm is too long")
        return value

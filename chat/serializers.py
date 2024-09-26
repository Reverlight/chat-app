from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from chat.models import Message, Thread


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Thread
        fields = ['id', 'participants', 'created', 'updated']

    def validate_participants(self, value):
        if len(value) != 2:
            raise ValidationError('Currently we support only two participants')
        return value


class MessageSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'thread', 'created', 'is_read']


class MessageUpdateSerializer(serializers.ModelSerializer):
    # Only is_read is supported for update
    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'thread', 'created', 'is_read']
        read_only_fields = ['sender', 'text', 'thread', 'created']

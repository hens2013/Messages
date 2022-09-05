from django.contrib.auth import authenticate
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from counter.models import Profile, Message


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'subject', 'creation_time', 'sender', 'read', 'receiver']


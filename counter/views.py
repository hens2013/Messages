
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
import requests
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from counter.models import Message, Profile
from counter.serializers import MessageSerializer, ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.models import model_to_dict


def index(request):
    return render(request, 'counter/index.html', {})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('user',)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        qs = super(ProfileViewSet, self).get_queryset()
        qs = qs.order_by("-id")
        return qs


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('user',)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        qs = super(MessageViewSet, self).get_queryset()
        qs = qs.order_by("-id")
        return qs

    def perform_create(self, serializer):
        super().perform_create(serializer)
        message: Message = serializer.instance
        serializer.save(user=message.sender, content=message.content, subject=message.subject,
                        creation_time=message.creation_time, receiver=message.receiver)


def getMessages(user, read):
    # user_messages = list(Message.objects.filter(sender=user).filter(read=read))
    user_messages = list(Message.objects.filter(sender=user))
    for index, msg in enumerate(user_messages):
        user_messages[index] = model_to_dict(msg)
    print(user_messages)
    return user_messages


@permission_classes((permissions.IsAuthenticated,))
@api_view(['GET'])
def message_read_per_user(request):
    if request.method == 'GET':
        try:
            user = is_user(request)
            if user:
                return HttpResponse(getMessages(user, False))
        except requests.ConnectionError:
            return HttpResponseNotFound('<h1>502 Bad Gateway server error response code</h1>')
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('<h1>Timeout error</h1>')
        except  Exception as e:
            return HttpResponseNotFound('Data not found')

        return HttpResponse('None')


def is_user(request):
    user = Profile.objects.filter(user_name=request.data['username'])[0]
    return user


@permission_classes((permissions.IsAuthenticated,))
@api_view(['GET'])
def message_unread_per_user(request):
    if request.method == 'GET':
        try:
            user = is_user(request)
            if user:
                return HttpResponse(getMessages(user, False))
        except requests.ConnectionError:
            return HttpResponseNotFound('<h1>502 Bad Gateway server error response code</h1>')
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('<h1>Timeout error</h1>')
        except  Exception as e:
            return HttpResponseNotFound('Data not found')

    return HttpResponseNotFound('Data not found')


@api_view(['GET'])
def read_message(request, message_id):
    if request.method == 'GET':
        try:
            message = Message.objects.get(id=message_id)
            if not message.read:
                message.read = True
                message.save()
                return JsonResponse({'Message': model_to_dict(message)})
            return HttpResponseNotFound('message already read ' + message.content)

        except requests.ConnectionError:
            return HttpResponseNotFound('<h1>502 Bad Gateway server error response code</h1>')
        except requests.exceptions.Timeout:
            return HttpResponseNotFound('<h1>Timeout error</h1>')
        except  Exception as e:
            return HttpResponseNotFound('Data not found')
    return HttpResponseNotFound('Data not found')

from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.ProfileViewSet)
router.register(r'messages', views.MessageViewSet)
urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api/message-read-per-user-id/<str:user_id>', views.message_read_per_user, name='message-read-per-user-id'),
    path('api/message-unread-per-user-id', views.message_unread_per_user,
         name='message-unread-per-user-id'),
    path('api/read-message/<str:message_id>', views.read_message,
         name='read-message'),
    path('api/delete-message/<str:message_id>', views.delete_message,
         name='delete-message')

]

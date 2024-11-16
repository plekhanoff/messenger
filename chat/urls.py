from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'users', UserProfileViewSet)

message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

message_detail = MessageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('profile/', UserProfileViewSet.as_view({'post': 'update_avatar'}), name='profile'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('index/', index, name='index'), 
    path('chat/<room_name>/', room, name="chat/room"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

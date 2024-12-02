from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.views import ChatViewSet, MessageViewSet, index, logout_view
from private_chat.views import chat_box
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'chat', ChatViewSet)
router.register(r'messages', MessageViewSet)

router.register(r'chatgroups/(?P<chat_pk>\d+)/messages', MessageViewSet, basename='chat-messages')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
    path('', include('chat.urls')),  
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index, name='index'), 
    path('logout/', logout_view, name='logout'),
    path("private_chat/<str:chat_box_name>/", chat_box, name="chat"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




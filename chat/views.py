
from rest_framework import viewsets
from .models import Chat, Message, UserProfile
from .serializers import ChatSerializer, MessageSerializer, UserProfileSerializer
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import SignUpForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.core.cache.backends.locmem import _caches as cache
from django.contrib.auth import logout
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from .forms import UserProfileForm



 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() 
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('profile.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('profile')

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/chats.html", {"room_name": room_name})

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.members.add(self.request.user)
        instance.save()
        

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        queryset = Message.objects.all()

        chat_group_pk = self.kwargs.get('chat_group_pk')
        if chat_group_pk is not None:
            queryset = queryset.filter(chat_id=chat_group_pk)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, chat_id=self.kwargs['chat_group_pk'])
        

class UserProfileViewSet(viewsets.ModelViewSet): 
    queryset = UserProfile.objects.all() 
    serializer_class = UserProfileSerializer 

    def update_avatar(self, request):
        user = request.user  
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES) 
            if form.is_valid():
                avatar = request.FILES.get('avatar/')  
                user.userprofile.avatar = avatar 
                user.userprofile.save() 
                return Response({"message": "Avatar updated successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            form = UserProfileForm()
        
        return Response({'form': form}, status=status.HTTP_400_BAD_REQUEST)

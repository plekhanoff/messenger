from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Chat(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    users = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.name
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message


class UserProfile(User):
    avatar = models.FileField(upload_to='avatar/', blank=True, null=True, default='default.png')
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
   
    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

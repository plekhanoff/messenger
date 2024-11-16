from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ClearableFileInput 
from .models import UserProfile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username','avatar',)
        widgets = {
            'avatar': ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'изображение'}),
         }
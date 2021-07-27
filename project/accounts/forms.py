from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', ]

class UpdateProfile(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class UpdateUser(ModelForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email',]


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):

    email = forms.EmailField(label = "Email",required=True, )

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
  
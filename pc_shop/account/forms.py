from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email',)


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

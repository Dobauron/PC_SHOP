from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account
from allauth.account.forms import SignupForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        return user

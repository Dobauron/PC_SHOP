from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Account
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")


class CustomSignupForm(SignupForm):
    def save(self, commit=True):
        user = super(CustomSignupForm, self).save(commit=False)
        if commit:
            user.save()
        return user



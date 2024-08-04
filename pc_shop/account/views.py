from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login

import logging

logger = logging.getLogger(__name__)


class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        print(email)
        password = form.cleaned_data.get('password')
        print(password)
        logger.debug(f'Trying to authenticate user with email: {email}')
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            logger.debug(f'Successfully authenticated usear with email: {email}')
            return super().form_valid(form)
        else:
            logger.debug(f'Failed to authenticate user with email: {email}')
            return self.form_invalid(form)


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('accounts:login')

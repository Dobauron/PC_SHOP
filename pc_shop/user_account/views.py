from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
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
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        logger.debug(f'Trying to authenticate user with email: {email}')
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            logger.debug(f'Successfully authenticated user with email: {email}')
            return super().form_valid(form)
        else:
            logger.debug(f'Failed to authenticate user with email: {email}')
            return self.form_invalid(form)


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('accounts:login')


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context


from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserDashboardView

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('', include('allauth.urls')),
]

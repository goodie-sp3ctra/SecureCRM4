# apps/accounts/urls.py
from django.urls import path
from .views import UserLoginView, user_logout, register, AdminLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/',      UserLoginView.as_view(),    name='login'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('logout/',     user_logout,                name='logout'),
    path('register/',   register,                   name='register'),
]

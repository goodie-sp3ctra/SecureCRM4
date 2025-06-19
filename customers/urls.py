# customers/urls.py
from django.urls import path
from . import views
from .views import (
    ClientListView, ClientDetailView,
    ClientCreateView, ClientUpdateView
)
from customers.views import UserLoginView, AdminLoginView
from django.contrib.auth.views import LogoutView

app_name = 'customers'   # ← this enables the namespace

urlpatterns = [
    path('',                ClientListView.as_view(), name='list'), 
    path("add/",            ClientCreateView.as_view(), name="add"),
    path("<int:pk>/",       ClientDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/",  ClientUpdateView.as_view(), name="edit"),
    path('',                views.home,            name='home'),
    path('add/',            views.add_customer,    name='add'),
    path('search/', views.CustomerSearchView.as_view(), name='search'),

    path("login/", UserLoginView.as_view(), name="login"),
    path("admin-login/", AdminLoginView.as_view(), name="admin_login"),

    # you can leave your existing logout (or swap in the generic)
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]



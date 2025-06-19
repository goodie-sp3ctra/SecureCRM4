# customers/urls.py
from django.urls import path
from . import views
from .views import (
    ClientListView, ClientDetailView,
    ClientCreateView, ClientUpdateView
)

app_name = 'customers'   # ← this enables the namespace

urlpatterns = [
    path('',                ClientListView.as_view(), name='list'), 
    path("add/",            ClientCreateView.as_view(), name="add"),
    path("<int:pk>/",       ClientDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/",  ClientUpdateView.as_view(), name="edit"),
    path('',                views.home,            name='home'),
    path('add/',            views.add_customer,    name='add'),
    path('search/', views.CustomerSearchView.as_view(), name='search'),
]



# apps/customers/urls.py
from django.urls import path
from .views import (
    ClientListView, ClientDetailView,
    ClientCreateView, ClientUpdateView,
    CustomerSearchView,
)

app_name = 'customers'

urlpatterns = [
    path('',                ClientListView.as_view(),   name='list'),
    path('add/',            ClientCreateView.as_view(), name='add'),
    path('<int:pk>/',       ClientDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/',  ClientUpdateView.as_view(), name='edit'),
    path('search/',         CustomerSearchView.as_view(),name='search'),
]
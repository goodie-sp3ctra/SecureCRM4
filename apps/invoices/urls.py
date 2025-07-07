# apps/invoices/urls.py
from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="list"),
    path("<int:pk>/",       views.InvoiceDetailView.as_view(), name="detail"),
    path("<int:pk>/send/",  views.InvoiceSendView.as_view(),   name="send"),
]
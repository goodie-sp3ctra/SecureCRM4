# apps/invoices/urls.py
from django.urls import path
from . import views
from crm_project.custom_admin import securecrm_admin_site  # custom admin site

app_name = "invoices"

urlpatterns = [
    path("admin/",        securecrm_admin_site.urls),   # custom admin
    path("", views.InvoiceListView.as_view(), name="list"),
    path("<int:pk>/",       views.InvoiceDetailView.as_view(), name="detail"),
    path("<int:pk>/send/",  views.InvoiceSendView.as_view(),   name="send"),
]
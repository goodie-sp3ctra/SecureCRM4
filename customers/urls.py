from django.urls import path
from .views import (
    home, 
    user_login, 
    user_logout, 
    register,
    CustomerList, 
    CustomerDetail, 
    add_customer, 
    search_customer,
    dashboard,
    account_details
)

urlpatterns = [
    # Home page (dashboard or welcome page)
    path('', home, name='home'),

    # Authentication
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),

    # Customer management
    path('customers/', CustomerList.as_view(), name='customer-list'),  # Customer list view
    path('customers/<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),  # Customer detail view
    path('customers/add/', add_customer, name='add_customer'),  # Add new customer
    path('customers/search/', search_customer, name='search_customer'),  # Search customers

    # Dashboard & Account Details
    path('dashboard/', dashboard, name='dashboard'),
    path('account-details/', account_details, name='account_details'),
]

# crm_project/urls.py
from django.contrib import admin
from django.urls import path, include
from customers import views as customer_views
from customers.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    # your home / auth / dashboard / account-details
    # path('',          customer_views.home,            name='home'),
    path("customers/", include(("customers.urls", "customers"), namespace="customers")),
    path('login/',    customer_views.user_login,      name='login'),
    path('logout/',   customer_views.user_logout,     name='logout'),
    path('register/', customer_views.register,        name='register'),

        path("", HomeView.as_view(template_name="home.html"), name="home"),
    path("customers/", include(("customers.urls", "customers"), namespace="customers")),

    path('dashboard/',       customer_views.dashboard,        name='dashboard'),
    path('account_details/', customer_views.account_details, name='account_details'),

    # mount the customers app, with namespace="customers"
    path(
        'customers/',
        include(
            ('customers.urls', 'customers.urls'),   # <-- (module, app_name)
            namespace='customers'
        )
    ),
]



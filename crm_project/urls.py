# crm_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns =[

    path("admin/", admin.site.urls),

    path(
        '', 
        include(('apps.website.urls', 'website'), namespace='website')
    ),

    path("dashboard/",include(("apps.dashboard.urls","dashboard"), namespace="dashboard")),

    # point at apps.customers, not customers
    path('customers/', include( ('apps.customers.urls', 'customers'), namespace='customers')
    ),

    path(
        "accounts/",
        include(
            ("apps.accounts.urls", "accounts"),  # module, app_name
            namespace="accounts"                 # then you can {% url 'accounts:login' %}
        ),
    ),
    path("jobs/", include(("apps.jobs.urls", "jobs"), namespace="jobs")),
    path("tasks/", include("apps.tasks.urls")),
    path("invoices/", include("apps.invoices.urls")),
    path("activity/", include(("apps.activity.urls", "activity"), namespace="activity"))
]
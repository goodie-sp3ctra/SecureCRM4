# crm_project/urls.py
from django.urls import path, include
from crm_project.custom_admin import securecrm_admin_site

urlpatterns =[
    path("secure-admin/", securecrm_admin_site.urls),
    path(
        '', 
        include(('apps.website.urls', 'website'), namespace='website')
    ),
    path("dashboard/",include(("apps.dashboard.urls","dashboard"), namespace="dashboard")),
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
    path("activity/", include(("apps.activity.urls", "activity"), namespace="activity")),
]
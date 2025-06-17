# customers/urls.py
from django.urls import path
from .views import ClientListView, ClientDetail, add_customer, search_customer

app_name = 'customers'   # ← this enables the namespace

urlpatterns = [
    path('',        ClientListView.as_view(), name='list'),    # customers:list
    path('add/',    add_customer,            name='add'),      # customers:add
    path('search/', search_customer,         name='search'),   # customers:search
    path('<int:pk>/', ClientDetail.as_view(), name='detail'),  # customers:detail
]


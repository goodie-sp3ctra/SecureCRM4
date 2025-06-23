from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('',      views.index, name='index'),  # GET /
    path('home/', views.home,  name='home'),   # GET /home/ → redirects to dashboard
    path('about/', views.about, name='about'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact/', views.contact, name='contact'),
]

# apps/website/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def home(request):
    # Now this can't loop back on itself!
    # Send signed-in users to your real dashboard view:
    return render(request, 'website/home.html')

def about(request):
    """About page (public)."""
    return render(request, 'website/about.html')

def pricing(request):
    """Pricing page (public)."""
    return render(request, 'website/pricing.html')

def contact(request):
    """Contact page (public)."""
    return render(request, 'website/contact.html')

def index(request):
    # marketing landing — even if logged in, show them this page
    return render(request, 'website/index.html')
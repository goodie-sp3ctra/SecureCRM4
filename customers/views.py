from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from django import forms
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Client
from .forms import ClientForm
import re

from .models import Client

# Password strength validator
def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'[0-9]', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )

# Home view
@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')

# Add Customer view
@login_required(login_url='/login/')
def add_customer(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        name = f"{first_name} {last_name}".strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password', '').strip()

        if not all([first_name, last_name, email, phone, address, password]):
            return render(request, 'customers/add_customer.html', {'error': 'All fields are required!'})

        if not re.fullmatch(r'\d{10}', phone):
            return render(request, 'customers/add_customer.html', {
                'error': 'Phone number must be exactly 10 digits.'
            })

        if not is_strong_password(password):
            return render(request, 'customers/add_customer.html', {
                'error': 'Password must be at least 8 characters long, include uppercase, lowercase, a number, and a symbol.'
            })

        if Client.objects.filter(email=email).exists():
            return render(request, 'customers/add_customer.html', {'error': 'A customer with this email already exists!'})

        try:
            hashed_password = make_password(password)
            Client.objects.create(
                name=name,
                email=email,
                phone_number=phone,
                address=address,
                password=hashed_password
            )
            return redirect('customer-list')
        except IntegrityError:
            return render(request, 'customers/add_customer.html', {
                'error': 'Something went wrong while saving the customer. Please try again.'
            })

    return render(request, 'customers/add_customer.html')

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'registration/login.html', {'form': form})

    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view
@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('login')

# Customer List View
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ClientListView(ListView):
    model = Client
    template_name = 'customers/client_list.html'
    context_object_name = 'client'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        customers = Paginator(self.get_queryset(), self.paginate_by).get_page(page)
        context['customers'] = customers
        return context

# Customer Detail View
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ClientDetail(DetailView):
    model = Client
    template_name = 'customers/client_detail.html'
    context_object_name = 'client'

# Search Customer View
@login_required(login_url='/login/')
def search_customer(request):
    query = request.GET.get('q', '')
    customers = Client.objects.filter(name__icontains=query) if query else Client.objects.all()
    return render(request, 'customers/search_customer.html', {'customers': customers, 'query': query})

# Dashboard View
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

# Account Details View
@login_required(login_url='/login/')
def account_details(request):
    return render(request, 'account_details.html')

# Root redirect to login
def root_redirect(request):
    return redirect('login')

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Client
from .forms import ClientForm

class ClientList(ListView):
    model = Client
    template_name = 'customers/client_list.html'
    context_object_name = 'clients'

class ClientCreate(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'customers/add_client.html'
    success_url = reverse_lazy('customers:list')

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name', 'contact_name', 'contact_email', 'phone', 'address', 'status']
        widgets = {
            'status': forms.Select(choices=Client.STATUS_CHOICES),
        }


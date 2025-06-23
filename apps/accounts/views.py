# apps/accounts/views.py

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
import re
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["admin_login"] = False
        return ctx

    def get_success_url(self):
        # where regular users go after login
        return self.get_redirect_url() or reverse_lazy("website:home")

class AdminLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_field_name = "next"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["admin_login"] = True
        return ctx

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            form.add_error(None, "You must be an admin to log in here.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        # where staff go after login; you could change to your admin dashboard URL
        return self.get_redirect_url() or reverse_lazy("website:home")

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/login.html', {'form': form})

    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('login')

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('accounts:login')
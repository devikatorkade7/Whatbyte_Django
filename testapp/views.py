from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from .forms import SignUpForm, PasswordChangeCustomForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'testapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'testapp/login.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'testapp/dashboard.html', {'username': request.user.username})

@login_required
def profile_view(request):
    return render(request, 'testapp/profile.html', {'user': request.user})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('dashboard')
    else:
        form = PasswordChangeCustomForm(user=request.user)
    return render(request, 'testapp/change_password.html', {'form': form})

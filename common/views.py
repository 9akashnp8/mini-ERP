from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .decorators import unauthenticated_user

@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "username OR password is Incorrect.")

    context = {}
    return render(request, 'common/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def admin_panel(request):
    return render(request, 'common/admin_panel_home.html')


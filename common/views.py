from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.urls import reverse

from .decorators import (
    unauthenticated_user,
    allowed_admins
)
from .permissions import AllowedGroupsMixin
from .forms import UserForm

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
@allowed_admins(allowed_admins=['employee-admin', 'hardware-admin', 'finance-admin'])
def admin_panel(request):
    return render(request, 'common/admin_panel_home.html')

class UserListCreateView(AllowedGroupsMixin, FormView):
    form_class = UserForm
    template_name = 'common/admin_panel/users_list.html'
    allowed_groups = ['employee-admin', 'hardware-admin', 'finance-admin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user })
        return kwargs

    def get_success_url(self) -> str:
        return reverse('user_list_create')

    def form_valid(self, form):
        groups = form.cleaned_data.pop("groups")
        user = User.objects.create(**form.cleaned_data)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.groups.set(groups)
        user.save()
        return super().form_valid(form)



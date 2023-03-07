from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# def admin_only(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         group = None
#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name
        
#         if group == 'employee':
#             return redirect('empprofile')
        
#         if group == 'admin':
#             return view_func(request, *args, **kwargs)
#     return wrapper_func

def allowed_admins(allowed_admins=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name__in=allowed_admins).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page! Login with an user account authorized to view this page.")
        return wrapper_func
    return decorator
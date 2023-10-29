from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_admins(allowed_admins=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name__in=allowed_admins).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied("You do not have permission to access this page.")
        return wrapper_func
    return decorator
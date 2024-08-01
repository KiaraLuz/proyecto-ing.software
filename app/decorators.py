from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_rol_admin:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("/")

    return wrapper

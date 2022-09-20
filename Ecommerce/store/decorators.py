from tokenize import group
from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticatedUser(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_func(request, *args, *kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            group = None
            if request.users.groups.exists():
                group = request.users.groups.all()[0].name

            if group.allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse('You are Not an Uathorized user')
        return wrapper_func
    return decorator

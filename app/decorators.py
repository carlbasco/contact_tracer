from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('checkin')
        else:    
            return view_func(request, *args, **kwargs)
    return wrapper_func

def restricted_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if group =='User':
            return redirect('place_create')
        elif group =='Admin':
           return view_func(request, *args, **kwargs)
    return wrapper_function
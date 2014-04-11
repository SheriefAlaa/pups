from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.views import login

def custom_login(request):
    '''
    Extends django's built-in login view to support redirecting already
    logged in users so that they can't view login.html if logged in.
    '''
    if request.user.is_authenticated():
        return redirect('/')

    return login(request, 'login.html', 'login')
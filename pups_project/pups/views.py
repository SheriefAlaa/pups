from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from pups.forms import ChangePassForm
from django.contrib import messages
from webchat.feedback import FeedbackMessages as fbm

def custom_login(request):
    '''
    Extends django's built-in login view to support redirecting already
    logged in users so that they can't view login.html if logged in.
    '''
    if request.user.is_authenticated():
        return redirect('/')

    return login(request, 'login.html', 'login')

@login_required
def change_password(request):
    form = ChangePassForm(request.POST or None)
        
    if form.is_valid(): # If all fields are valid change the password
        if form.change_password(request, form.cleaned_data):
            messages.add_message(request, messages.INFO, fbm.good_pw)
            return redirect('/chpass')
            
        messages.add_message(request, messages.INFO, fbm.bad_pw)

    return render(request, 'change_password.html', {'form' : form})
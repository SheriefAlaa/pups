from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from webchatapp.models import LoginForm, ChangePassForm, Token
from webchatapp.feedback import FeedbackMessages as fbm
from webchatapp import settings

def login(request):
    login_form = LoginForm()
    if request.user.is_authenticated():
        return redirect('/logged')

    if request.method != 'POST':
    # First visit to the login page.
        return render(request, 'login.html', {'form' : login_form} )
    else:
        # User trying to login.
        user = auth.authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))

    if user is not None:
        # Successful login, redirect to the token management page.
        auth.login(request, user)
        return redirect('/tokens')
    else:
        messages.add_message(request, messages.INFO, fbm.bad_login )
        return render(request, 'login.html', {'form': login_form } ) # bad login.

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        messages.add_message(request, messages.INFO, fbm.was_logged)
        return redirect('/login')
    else:
        messages.add_message(request, messages.INFO, fbm.not_logged)
        return redirect('/login')

def change_password(request):
    if request.user.is_authenticated():  
        form = ChangePassForm(request.POST or None)
            
        if form.is_valid(): # If all fields are valid change the password
            if form.change_password(request, form.cleaned_data):
                messages.add_message(request, messages.INFO, fbm.good_pw)
                return redirect('/chpass')
            else:
                messages.add_message(request, messages.INFO, fbm.bad_pw)

        return render(request, 'change_password.html', {'form' : form})
    else:
        return redirect('/login') # Not logged in


def logged_in(request):
    return redirect('/tokens')

def tokens_page(request):
    token = Token()
    params = {
        'name' : request.user.username,
        'tokens' : token.get_assistant_tokens(User.objects.get(id = request.user.id)),
        'server' : settings.CONFIG['server']
    }

    # View all tokens owned by logged in assistant
    if request.user.is_authenticated():
            return render(request, 'tokens.html', params )
    else:
        return redirect('/login')

    # Create one token
    if 'create_token' in request.POST:
        query = token.create_token(request.user.id, settings.CONFIG['expiration_days'], request.POST.get('comment', ''))
        if query:
            messages.add_message(request, messages.INFO, fbm.token_created)
            return redirect('/tokens')
        else:
            messages.add_message(request, messages.INFO, fbm.db_error)
            return redirect('/tokens')

    # Deletes one or more tokens
    if 'delete' in request.POST:
        # If nothing was selected
        if len(request.POST.getlist("selected_list")) == 0:
            messages.add_message(request, messages.INFO, fbm.empty_list)
            return redirect('/tokens')
            
        if token.delete_token(request.POST.getlist("selected_list")):
            messages.add_message(request, messages.INFO, fbm.delete_passed)
            return redirect('/tokens')
        else:
            messages.add_message(request, messages.INFO, fbm.delete_failed)
            return redirect('/tokens')

########### Client side views ###########
def chat(request, token):
    t = Token()
    t_obj = t.get_token(token)

    if t_obj:
        params = {
            'server' : settings.CONFIG['server'],
            'bosh' : settings.CONFIG['bosh'],
            'receiver' : t_obj.owner.username + settings.CONFIG['receiver'],
            'receiver_name' : t_obj.owner.username,
            'token' : token
        }
        return render(request, 'prodromus.html', params)
    else:
        return HttpResponse("This is not a vaild chat token")

def home(request):
    return render(request, 'index.html')
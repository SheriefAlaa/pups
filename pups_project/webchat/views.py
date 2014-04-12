from django.http import HttpResponse
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from webchat.models import Token
from webchat.forms import ChangePassForm
from webchat.feedback import FeedbackMessages as fbm
from pups import settings

@login_required
def change_password(request):

    form = ChangePassForm(request.POST or None)
        
    if form.is_valid(): # If all fields are valid change the password
        if form.change_password(request, form.cleaned_data):
            messages.add_message(request, messages.INFO, fbm.good_pw)
            return redirect('/chpass')
        else:
            messages.add_message(request, messages.INFO, fbm.bad_pw)

    return render(request, 'change_password.html', {'form' : form})

@login_required
def tokens_page(request):
    token = Token()
    params = {
        'name' : request.user.username,
        'tokens' : token.get_assistant_tokens(User.objects.get(id = request.user.id)),
        'server' : settings.CONFIG['server']
    }

    # View all tokens owned by logged in assistant
    if 'create_token' in request.POST:
        create_token(request)

    # Deletes one or more tokens
    if 'delete' in request.POST:
        delete_token(request)

    return render(request, 'tokens.html', params )

def create_token(request):
    token = Token()

    if token.create_token(request.user.id, settings.CONFIG['expiration_days'], request.POST.get('comment', '')):
        messages.add_message(request, messages.INFO, fbm.token_created)
        return redirect('/tokens')
    else:
        messages.add_message(request, messages.INFO, fbm.db_error)
        return redirect('/tokens')

def delete_token(request):
    token = Token()

    # If nothing was selected redirect and complain
    if len(request.POST.getlist("selected_list")) == 0:
        messages.add_message(request, messages.INFO, fbm.empty_list)
        return redirect('/tokens')

    # Delete tokens inside the list or redirect if can't access db.
    if token.delete_token(request.POST.getlist("selected_list")):
        messages.add_message(request, messages.INFO, fbm.delete_passed)
        return redirect('/tokens')
    else:
        messages.add_message(request, messages.INFO, fbm.delete_failed)
        return redirect('/tokens')

########### Client side views ###########
def chat(request, token):
    '''
    Offers a chat session though Prodromus-client if the token exists
    and did not expire.
    '''

    t = Token()
    t_obj = t.get_token(token)

    if t_obj:
        # Make sure token didn't expire
        if t_obj.expires_at >  timezone.now():
            params = {
                'server' : settings.CONFIG['server'],
                'bosh' : settings.CONFIG['bosh'],
                'receiver' : t_obj.owner.username + settings.CONFIG['receiver'],
                'receiver_name' : t_obj.owner.username,
                'token' : token
            }
            return render(request, 'prodromus.html', params)
        else:
            return HttpResponse("This token expired, please email help@rt.torproject to get a new one.")
    else:
        # Token is invalid (wrong input)
        return HttpResponse("This is not a vaild chat token")

def home(request):
    return render(request, 'index.html')
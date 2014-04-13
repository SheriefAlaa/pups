from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from webchat.feedback import FeedbackMessages as fbm
from webchat.models import Token
from pups import settings

@login_required
def tokens_page(request):
    token = Token()
    
    # Create one token
    if 'create_token' in request.POST:
        return create_token(request)

    # Revoke one or more tokens
    if 'revoke' in request.POST:
        return revoke_token(request)

    params = {
        'name' : request.user.username,
        'tokens' : token.get_assistant_tokens(User.objects.get(id = request.user.id)),
        'server' : settings.CONFIG['server']
    }
    # View all tokens owned by logged in assistant
    return render(request, 'tokens.html', params )

def create_token(request):
    token = Token()

    if token.create_token(request.user.id, settings.CONFIG['expiration_days'], request.POST.get('comment', '')):
        messages.add_message(request, messages.INFO, fbm.token_created)
        return redirect('/tokens')
    else:
        messages.add_message(request, messages.INFO, fbm.db_error)
        return redirect('/tokens')

def revoke_token(request):
    token = Token()

    # If nothing was selected redirect and complain
    if len(request.POST.getlist("selected_list")) == 0:
        messages.add_message(request, messages.INFO, fbm.empty_list)
        return redirect('/tokens')

    # Delete tokens inside the list or redirect if can't access db.
    if token.revoke_token(request.POST.getlist("selected_list")):
        messages.add_message(request, messages.INFO, fbm.revoke_success)
        return redirect('/tokens')
    else:
        messages.add_message(request, messages.INFO, fbm.db_error)
        return redirect('/tokens')

def chat(request, token):
    '''
    Offers a chat session though Prodromus-client if the token exists
    and did not expire.
    '''

    t = Token()
    t_obj = get_object_or_404(Token, token = token)

    # Make sure token didn't expire
    if t_obj.expires_at < timezone.now():
        return render(request, "token_exp.html")
        
    params = {
        'server' : settings.CONFIG['server'],
        'bosh' : settings.CONFIG['bosh'],
        'receiver' : t_obj.owner.username + settings.CONFIG['receiver'],
        'receiver_name' : t_obj.owner.username,
        'token' : token
    }
    return render(request, 'prodromus.html', params)

def home(request):
    return render(request, 'index.html')
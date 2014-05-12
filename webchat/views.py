# This file is part of Pups, a django/python project which contains
# web support tools
#
#  Author: Sherief Alaa <sheriefalaa.w@gmail.com>
#
#  Copyright:
#   © 2014 Sherief Alaa.
#   © 2014 The Tor Project, Inc.
#
# Pups is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pups is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pups.  If not, see <http://www.gnu.org/licenses/>.

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
        return revoke_tokens(request)

    params = {
        'name': request.user.username,
        'tokens': token.get_assistant_tokens(
            User.objects.get(id=request.user.id)),
        'server': settings.CONFIG['server']
    }
    # View all tokens owned by logged in assistant
    return render(request, 'tokens.html', params)


def create_token(request):
    token = Token()

    if not token.create_token(request.user.id,
                              settings.CONFIG['expiration_days'],
                              request.POST.get('comment', '')):

        messages.add_message(request, messages.INFO, fbm.db_error)
        return redirect('/tokens')

    messages.add_message(request, messages.INFO, fbm.token_created)
    return redirect('/tokens')


def revoke_tokens(request):
    token = Token()

    # If nothing was selected redirect and complain
    if len(request.POST.getlist("selected_list")) == 0:
        messages.add_message(request, messages.INFO, fbm.empty_list)
        return redirect('/tokens')

    # Revoke a token or more
    token.revoke_tokens(request.POST.getlist("selected_list"))
    messages.add_message(request, messages.INFO, fbm.revoke_success)
    return redirect('/tokens')


def chat(request, token):
    '''
    Offers a chat session though Prodromus-client if the token exists
    and did not expire.
    '''

    t = Token()
    t_obj = get_object_or_404(Token, token=token)

    # Make sure token didn't expire
    if t_obj.expires_at < timezone.now():
        return render(request, "token_exp.html")

    params = {
        'server': settings.CONFIG['server'],
        'bosh': settings.CONFIG['bosh'],
        'receiver': t_obj.owner.username + settings.CONFIG['receiver'],
        'receiver_name': t_obj.owner.username,
        'token': token
    }
    return render(request, 'prodromus.html', params)


def index(request):
    '''
    Explains what is webchat to the user and how to use it in all
    help desk languages.
    '''
    return render(request, 'index.html')

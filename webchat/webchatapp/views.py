from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from webchatapp.models import LoginForm, ChangePassForm, Token
from webchatapp.feedback import FeedbackMessages as fbm

# TODO:
# Client side functions (home, check_token and chat)

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
    chpass_form = ChangePassForm()

    if request.user.is_authenticated():
        if request.method != 'POST':
            return render(request, 'change_password.html', {'form' : chpass_form})
    else:
        return redirect('/login')

    if request.method == 'POST':
        # Compare new passwords and check if current_pass is correct and save.
        if chpass_form.save(request, request.POST.get('current_pass', ''), request.POST.get('new_pass', ''), request.POST.get('new_pass_confirm', '')):
            messages.add_message(request, messages.INFO, fbm.good_pw )
            return render(request, 'change_password.html', {'form' : chpass_form} )
        else:
            messages.add_message(request, messages.INFO, fbm.bad_pw )
            return render(request, 'change_password.html', {'form' : chpass_form} )
    else:
        return redirect('/login')

def logged_in(request):
    return redirect('/tokens')

def tokens_page(request):

    EXPIRATION_DAYS = 3
    token = Token()
    params = {
        'name' : request.user.username,
        'tokens' : token.get_assistant_tokens(User.objects.get(id = request.user.id)),
    }

    # View state: all tokens owned by logged in assistant
    if request.user.is_authenticated():
        if request.method != 'POST':
            return render(request, 'tokens.html', params )
    else:
        return redirect('/login')

    # Create one token
    if 'create_token' in request.POST:
        ticket_id = request.POST.get('rt_ticket', '')
        if token.exists(ticket_id):
            messages.add_message(request, messages.INFO, fbm.ticket_exists)
            return redirect('/tokens')

        if ticket_id.isdigit():
            query = token.create_token(request.user.id, EXPIRATION_DAYS, ticket_id)
            if query:
                messages.add_message(request, messages.INFO, fbm.ticket_created)
                return redirect('/tokens')
            else:
                messages.add_message(request, messages.INFO, fbm.db_error)
                return redirect('/tokens')
        else:
            messages.add_message(request, messages.INFO, fbm.bad_ticket_format)
            return redirect('/tokens')

    # Deletes one or more tokens
    if 'delete' in request.POST:
        # If nothing was selected
        if len(request.POST.getlist("ticket_list")) == 0:
            messages.add_message(request, messages.INFO, fbm.empty_list)
            return redirect('/tokens')
            
        if token.delete_token(request.POST.getlist("ticket_list")):
            messages.add_message(request, messages.INFO, fbm.delete_passed)
            return redirect('/tokens')
        else:
            messages.add_message(request, messages.INFO, fbm.delete_failed)
            return redirect('/tokens')

    # Enter Edit state
    if "edit" in request.POST:
        # If nothing was selected
        if len(request.POST.getlist("ticket_list")) == 0:
            messages.add_message(request, messages.INFO, fbm.empty_list)
            return redirect('/tokens')

        # Remember what got selected for editing
        request.session['to_edit_list'] = token.parse_to_int(request.POST.getlist("ticket_list"))
        params.update({ 'to_edit_list' : request.session['to_edit_list'], 'edit_state' : True })
        return render(request, 'tokens.html', params)

    # Save the edited tickets and go back to view state
    if "save" in request.POST:
        query = token.update_tokens(request.POST.getlist('original_ticket_list'), request.POST.getlist('modified_ticket_list'))

        if query == True:
            messages.add_message(request, messages.INFO, fbm.edit_pass)
            return render(request, 'tokens.html', params)
        else:
            # Failure message: Some of the $tickets you are trying to edit are already taken by another assistant
            query.insert(0, fbm.edit_failed)
            for msg in query:
                messages.add_message(request, messages.INFO,  msg)
            return redirect('/tokens')

########### Client side views ###########
def not_found(request):
    return render(request, '404.html')


def home(request):
    return render(request, 'index.html')

# check_token will be triggered when someone visits
# webchat.torproject.org/chat/32digitsandnumberscode

def check_token(request):
    return HttpResponse("Checking token...")

# if the user passed checkToken then let the user
# enter his name and chat with an Assistant.
def chat(request):
    return render(request, 'prodromus.html')
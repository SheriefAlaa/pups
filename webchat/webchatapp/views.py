from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from webchatapp.models import LoginForm, ChangePassForm, Token

# TODO:
# Unify feedback messages using django's messages framework.
# Client side functions (home, check_token and chat)

def login(request):
	form = LoginForm()

	if request.user.is_authenticated():
		return redirect('/logged')

	if request.method != 'POST':
		# First visit to the login page.
		return render(request, 'login.html', {'form' : form} )
	else:
		# User trying to login.
		user = auth.authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))

		if user is not None:
			# Successful login, redirect to the token management page.
			auth.login(request, user)
			return redirect('/tokens')
		else:
			# Incorrect username/password, display an error.
			return render(request, 'login.html', {'form': form , 'bad_login' : True} ) # bad login.

def logout(request):
	if request.user.is_authenticated():
		auth.logout(request)
		return render(request, 'logout.html', {'was_logged' : True})
	else:
		auth.logout(request)	
		return render(request, 'logout.html', {'was_not_logged' : True})

def change_password(request):
	form = ChangePassForm()
	if request.user.is_authenticated():
		return render(request, 'change_password.html', {'form' : form})

		if request.method == 'POST':
			# Compare new passwords and check if current_pass is correct and save.
			if form.save(request, request.POST.get('current_pass', ''), request.POST.get('new_pass', ''), request.POST.get('new_pass_confirm', '')):
				data = ( {'form' : form, 'success' : True} )
				return render(request, 'change_password.html', data )
			else:
				data = ( {'form' : form, 'mismatch' : True} )
				return render(request, 'change_password.html', data )
	else:
		return redirect('/login')

def logged_in(request):
	return redirect('/tokens')

def tokens_page(request):
	
	EXPIRATION_DAYS = 3
	token = Token()

	# Viewing all tokens owned by logged in assistant
	if request.user.is_authenticated():
		if request.method != 'POST':
			data = token.get_assistant_tokens(User.objects.get(id = request.user.id))
			return render(request, 'tokens.html', {'name' : request.user.username, 'tokens' : data} )
	else:
		return redirect('/login')

	# Create one token
	if 'create_token' in request.POST:
		ticket_id = request.POST.get('rt_ticket', '')
		if token.exists(ticket_id):
			# Leave a message: RT_ticket exists
			return redirect('/tokens')
		elif ticket_id.isdigit() and token.create_token(request.user.id, EXPIRATION_DAYS, ticket_id):
			# Leave a message that the token was successfully saved.
			return redirect('/tokens')
		else:
			# Failed. reason: either RT ticket contains letters or cannot query db.
			return redirect('/tokens')

	# Deletes one or more tokens
	if 'delete' in request.POST:
		if token.delete_token(request.POST.getlist("ticket_list")):
			return redirect('/tokens') #report success
		else:
			return redirect('/tokens') #report failure
	
	# Enter the Edit state
	if "edit" in request.POST:
		# Remember what got selected for editing
		request.session['to_edit_list'] = token.parse_to_int(request.POST.getlist("ticket_list"))
		params = {
			'name' : request.user.username,
			'tokens' : token.get_assistant_tokens(User.objects.get(id = request.user.id)),
			'to_edit_list' : request.session['to_edit_list'],
			'edit_state' : True,
		}
		return render(request, 'tokens.html', params)

	# Save the edited tickets and go back to view state
	if "save" in request.POST:
		query = token.update_tokens(request.POST.getlist('original_ticket_list'), request.POST.getlist('modified_ticket_list'))

		if query:
			params = {
				'name' : request.user.username,
				'tokens' : token.get_assistant_tokens(User.objects.get(id = request.user.id))
			}
			return render(request, 'tokens.html', params)
		else:
			# Failure message: Some of the $tickets you are trying to edit are already taken by another assistant
			return redirect('/logged')

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
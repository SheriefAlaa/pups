from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from webchat.models import LoginForm, ChangePassForm, Token
from django.contrib import auth
from django.contrib.auth.models import User
import uuid
from datetime import date, timedelta
from django.contrib import messages
from webchat.utils import is_message

def login(request):
	if request.user.is_authenticated():
		return redirect('/logged')

	if request.method != 'POST':
		# First visit to the login page.
		form = LoginForm()
		return render(request, 'login.html', {'form' : form} )
	else:
		# User trying to login.
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)

		if user is not None:
			# Successful login, redirect to the token management page.
			auth.login(request, user)
			return redirect('/tokens')
		else:
			# Incorrect username/password, display an error.
			form = LoginForm()
			return render(request, 'login.html', {'form': form , 'bad_login' : True} ) # Handles bad login.

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
		if request.method != 'POST':
			data = ( {'form' : form} )
			return render(request, 'change_password.html', data)
		else:
			current_pass = request.POST.get('current_pass', '')
			new_pass = request.POST.get('new_pass', '')
			new_pass_confirm = request.POST.get('new_pass_confirm', '')

			# Compare new passwords and check if current_pass is correct and save.
			if (new_pass == new_pass_confirm) and request.user.check_password(current_pass):
				request.user.set_password(new_pass)
				request.user.save()
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

	data = Token.objects.filter(owner = User.objects.get(id = request.user.id))

	if request.user.is_authenticated():
		return render(request, 'tokens.html', {'name' : request.user.username, 'id' : request.user.id, 'tokens' : data } )
	else:
		return redirect('/login')
	

def create_token(request):
	expiration_days_count = 3

	if request.user.is_authenticated():
		if request.method == 'POST':
			ticket_id = request.POST.get('rt_ticket', '')

			try:
			 	Token.objects.get(rt_ticket = ticket_id)
				# Ticket already exists
				return redirect('/tokens')
			except:
				pass

			if ticket_id.isdigit():
				token_query = Token(
					owner = User.objects.get(id = request.user.id),
				 	token = uuid.uuid4().hex,
				 	created = date.today(), 
				 	expires = date.today() + timedelta(expiration_days_count),
				 	rt_ticket = ticket_id
				 	)

				if (token_query.save()):
					request.session['token_saved'] = True
				else:
					request.session['token_saved'] = False
				# Save and report success
				return redirect('/tokens')
			else:
				# Say RT tickets need to be numbers only.
				return redirect('/tokens')
		else:
			# Say nothing happened, request needs to be POST
			return redirect('/tokens')
	# Say session expired
	return redirect('/login')

def edit_token(request):
	'''
	Handles Edit RT ticket, Delete a whole row
	'''
 	moo = request.POST.getlist("ticket_list")
	# also set some session variable to report success.
	return render(request, 'test_page.html', {'moo' : moo})

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
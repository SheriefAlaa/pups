from django.http import HttpResponse
from django.shortcuts import render, redirect
from webchat.models import LoginForm, ChangePassForm
from django.contrib import auth


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


def tokens(request):
	if request.user.is_authenticated():
		return render(request, 'tokens.html', {'name' : request.user.username} )
	else:
		return redirect('/login')
	

#def delete_token(token):
#def create_token()
#def edit_token()
#def view_tokens(sa_id)


def not_found(request):
	return render(request, '404.html')


def logged_in(request):
	return HttpResponse("Hi, you are already logged in, would you like to Logout?")



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
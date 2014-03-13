from django.db import models
from django.contrib.auth.models import User
from django import forms
import uuid
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist

class Token(models.Model):
	t_id  = models.AutoField(primary_key=True)
	owner = models.ForeignKey(User)
	token = models.CharField(max_length=64)
	created = models.DateField()
	expires = models.DateField()
	rt_ticket = models.CharField(max_length=30)

	def __unicode__(self):
		return u'ID: %s Owner: %s Ticket: %s' % (self.t_id, self.owner, self.rt_ticket)

	def data(self):
		return{'t_id' : self.t_id, 'ticket': self.rt_ticket, 'token' : self.token, 'created' : self.created, 'expires' : self.expires}

	def create_token(self, owner_id, expiration_days, ticket_id):
		q = Token(
					owner = User.objects.get(id = owner_id),
					token = uuid.uuid4().hex,
					created = date.today(), 
					expires = date.today() + timedelta(expiration_days),
					rt_ticket = ticket_id
					)
		if q.save():
			return True
		else:
			return False

	def update_tokens(self, original_ticket_list, modified_ticket_list):
		'''
		This function will first check if any items in modified_ticket_list
		already exist in the database, if so it will return the bad ticket
		in a dict, if not, it will update the database using 
		original_ticket_list and return True
		'''
		result = []
		for rt_ticket in modified_ticket_list:
			if self.exists(rt_ticket):
				result.append(rt_ticket)

		# Found that someone already took a ticket you are trying to modify
		if len(result) != 0:
			return result
		
		# Update
		for i in range(len(original_ticket_list)):
			Token.objects.filter(rt_ticket = original_ticket_list[i]).update(rt_ticket = modified_ticket_list[i])
		return True

	def delete_token(self, t_id_list):
		count = 0

		for t_id in t_id_list:
			token = Token.objects.get(t_id = t_id)
			if token is not None:
				count = count + 1
				token.delete()
		if count == len(t_id_list):
			return True
		else:
			return False

	def exists(self, ticket_id):
		try:
			token = Token.objects.get(rt_ticket = ticket_id)
		except ObjectDoesNotExist:
			return False
		return True

	def get_assistant_tokens(self, assistant):
		return Token.objects.filter(owner = assistant)

	def parse_to_int(self, edit_list):
		result = []
		for i in edit_list:
			result.append(int(i))
		return result


class LoginForm(forms.Form):
	username = forms.CharField(max_length=32)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class ChangePassForm(forms.Form):
	current_pass = forms.CharField(max_length=32, widget=forms.PasswordInput)
	new_pass = forms.CharField(max_length=32, widget=forms.PasswordInput)
	new_pass_confirm = forms.CharField(max_length=32, widget=forms.PasswordInput)

	def save(self, request, current_pass, new_pass, new_pass_confirm):
		if (new_pass == new_pass_confirm) and request.user.check_password(current_pass):
			request.user.set_password(new_pass)
			request.user.save()		
			return True
		else:
			return False
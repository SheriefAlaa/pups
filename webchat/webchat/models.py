from django.db import models
from django import forms

class Assistant(models.Model):
	sa_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	password = models.CharField(max_length=256)

class Token(models.Model):
	t_id  = models.AutoField(primary_key=True)
	owner = models.ForeignKey(Assistant)
	token = models.CharField(max_length=64)
	created = models.DateField()
	expires = models.DateField()
	rt_ticket = models.CharField(max_length=30)

class LoginForm(forms.Form):
	username = forms.CharField(max_length=32)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class ChangePassForm(forms.Form):
	current_pass = forms.CharField(max_length=32, widget=forms.PasswordInput)
	new_pass = forms.CharField(max_length=32, widget=forms.PasswordInput)
	new_pass_confirm = forms.CharField(max_length=32, widget=forms.PasswordInput)
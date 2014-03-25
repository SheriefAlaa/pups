from django.db import models
from django.contrib.auth.models import User
from django import forms
import uuid
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

class Token(models.Model):
    t_id  = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    token = models.CharField(max_length=64)
    created = models.DateTimeField()
    expires = models.DateTimeField()
    comment = models.CharField(max_length=128)

    def __unicode__(self):
        return u'ID: %s Owner: %s' % (self.t_id, self.owner)

    def create_token(self, owner_id, expiration_days, comment):
        q = Token(
                    owner = User.objects.get(id = owner_id),
                    token = uuid.uuid4().hex,
                    created = datetime.now(), 
                    expires = datetime.now() + timedelta(expiration_days),
                    comment = comment
                    )
        q.save()

        if q.t_id:
            return True
        else:
            return False

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

    def get_assistant_tokens(self, assistant):
        return Token.objects.filter(owner = assistant).order_by('-t_id')

    def get_token(self, token):
        try:
            q = Token.objects.get(token = token)
        except ObjectDoesNotExist:
            return []
        return q

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
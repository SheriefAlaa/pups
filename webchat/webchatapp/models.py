import uuid
from datetime import datetime, timedelta
from django.db import models
from django import forms
from django.contrib.auth.models import User
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

        return q.t_id is not None

    def get_token(self, token):
        try:
            Token.objects.get(token = token)
        except ObjectDoesNotExist:
            return []
        return Token.objects.get(token = token)

    def delete_token(self, t_id_list):
        
        # Keeps track of how many items were deleted from the DB
        delete_count = 0

        for t_id in t_id_list:
            token = get_token(t_id)
            if token:
                delete_count = delete_count + 1
                token.delete()
        # Returns True if all selected tokens were deleted and false if not
        return count == len(t_id_list) 

    def get_assistant_tokens(self, assistant):
        return Token.objects.filter(owner = assistant).order_by('-t_id')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class ChangePassForm(forms.Form):
    current_pass = forms.CharField(max_length=32, widget=forms.PasswordInput)
    new_pass = forms.CharField(max_length=32, widget=forms.PasswordInput)
    new_pass_confirm = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def change_password(self, request, data):
        if (data['new_pass'] == data['new_pass_confirm'] ) and \
            request.user.check_password(data['current_pass'] ):

            request.user.set_password(data['new_pass'])
            request.user.save()
            return True
        else:
            return False
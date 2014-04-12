import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Token(models.Model):
    t_id  = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add = True)
    expires_at = models.DateTimeField()
    comment = models.CharField(max_length=128)

    def __unicode__(self):
        return u'ID: %s Owner: %s' % (self.t_id, self.owner)

    def create_token(self, owner_id, expiration_days, comment):
        q = Token(
                    owner = User.objects.get(id = owner_id),
                    token = uuid.uuid4().hex,
                    expires_at = timezone.now() + timedelta(expiration_days),
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

    def revoke_token(self, token_list):
        '''
        Sets the expiration date equals to the creation date of a token or more
        '''
        success = True

        for token in token_list:
            token = self.get_token(token)
            if token and (success == True):
                token.expires_at = token.created_at
                token.save()
            else:
                return False
        return True

    def get_assistant_tokens(self, assistant):
        return Token.objects.filter(owner = assistant).order_by('-t_id')
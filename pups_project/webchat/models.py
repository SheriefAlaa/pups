import uuid
from datetime import datetime, timedelta
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
                    expires_at = datetime.now() + timedelta(expiration_days),
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

    def delete_token(self, token_list):
        # Keeps track of how many items were deleted from the DB
        delete_count = 0
        for token in token_list:
            token = self.get_token(token)
            if token:
                delete_count = delete_count + 1
                token.delete()
        # Returns True if all selected tokens were deleted and false if not
        return delete_count == len(token_list) 

    def get_assistant_tokens(self, assistant):
        return Token.objects.filter(owner = assistant).order_by('-t_id')
import datetime
from django.db import models
from django.contrib.auth.models import User
from webchat.models import Token
from stats.models import Issue


def get_home_stats(uid, month=datetime.datetime.now().month):

    owner = User.objects.get(id=uid)
    tokens = Token.objects.filter(owner=owner).filter(
        expires_at__month=datetime.datetime.now().month)

    data = {}
    data['user'] = owner.username
    data['live_tokens'] = Token.get_live_tokens(owner, month)
    data['expired_tokens'] = Token.get_expired_tokens(owner, month)
    data['revoked_tokens'] = Token.get_revoked_tokens(owner, month)
    data['total_visits'] = Token.get_token_visits(owner, month)

    data['frequent_issues'] = Issue.objects.filter(
        created_by=owner.username).count()

    return data


def get_uid_list():
    uid_list = User.objects.all()
    return uid_list

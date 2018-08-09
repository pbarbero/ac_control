from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class ButtonPush(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET(get_sentinel_user))
    datetime = models.DateTimeField(auto_now_add=True)

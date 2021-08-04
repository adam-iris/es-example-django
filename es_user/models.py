from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from es_user.lib import get_jwt
from logging import getLogger

LOGGER = getLogger(__name__)


class UserJWT(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    jwt = models.JSONField(encoder=DjangoJSONEncoder)
    created = models.DateTimeField(auto_now_add=False)


@receiver(user_logged_in)
def on_user_logged_in(request=None, user=None, **kwargs):
    """
    Handle a user login
    """
    UserJWT.objects.filter(user=user).delete()
    user_jwt = get_jwt(request)
    LOGGER.info("user_logged_in user=%s jwt=%s", user, jwt)
    if user_jwt:
        UserJWT.objects.create(user=user, jwt=user_jwt)        


@receiver(user_logged_out)
def on_user_logged_out(user=None, **kwargs):
    """
    Handle a user logout
    """
    LOGGER.info("user_logged_out user=%s", user)
    UserJWT.objects.filter(user=user).delete()
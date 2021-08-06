from logging import getLogger

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.dispatch import receiver

from es_user.vouch_proxy import VouchProxyJWT

LOGGER = getLogger(__name__)


class UserJWT(models.Model):
    """
    Cached version of the JWT token received from VouchProxy.
    """
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    jwt = models.JSONField(encoder=DjangoJSONEncoder)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    @classmethod
    def create_from_request(cls, request, user=None):
        """
        Create from the given request
        """
        vp_jwt = VouchProxyJWT(request=request)
        if vp_jwt.is_valid():
            return cls.objects.create(
                user=(user or request.user),
                jwt=vp_jwt.value,
                active=True,
            )

    @classmethod
    def get_all_user_claims(cls, user):
        """
        Extract all the claims for the given user
        """
        claims = {}
        user_jwts = cls.objects.filter(user=user).all()
        for user_jwt in user_jwts:
            for k, v in user_jwt.jwt.get('CustomClaims', {}).items():
                existing = claims.setdefault(k, [])
                if v not in existing:
                    existing.append(v)
        return claims


@receiver(user_logged_in)
def on_user_logged_in(request=None, user=None, **kwargs):
    """
    Handle a user login
    """
    if user and user.pk:
        # UserJWT.objects.filter(user=user).delete()
        user_jwt = UserJWT.create_from_request(request)
        LOGGER.info("user_logged_in user=%s jwt=%s", user, user_jwt)


@receiver(user_logged_out)
def on_user_logged_out(user=None, **kwargs):
    """
    Handle a user logout
    """
    if user and user.pk:
        LOGGER.info("user_logged_out user=%s", user)
        UserJWT.objects.filter(user=user).update(active=False)

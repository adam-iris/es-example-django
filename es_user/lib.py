import base64
import gzip
import json
import logging

import jwt
import requests
from django.conf import settings

LOGGER = logging.getLogger(__name__)


def get_jwt(request):
    """
    Get the JWT data from the vouch-proxy cookie
    """
    cookie_name = 'VouchCookie'
    cookie = request.COOKIES.get('VouchCookie')
    if cookie:
        try:
            validate = requests.get(
                settings.VOUCH_PROXY_VALIDATE_ENDPOINT,
                cookies={cookie_name: cookie},
                verify=False,
            )
            validate.raise_for_status()

            # Vouch cookie is URL-safe Base64 encoded Gzipped data
            decompressed = gzip.decompress(base64.urlsafe_b64decode(cookie))
            payload = jwt.decode(decompressed, options={'verify_signature': False})
            return payload
        except Exception as e:
            LOGGER.error("Failed to get JWT: %s", e)
    return None

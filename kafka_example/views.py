from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django import forms
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from kafka_example.kafka.producer import produce_example_message
from kafka_example.models import ExampleValue
from django.contrib.auth import logout
import gzip
import base64
import jwt
import requests
import logging
import json

LOGGER = logging.getLogger(__name__)


class TestForm(forms.ModelForm):
    """
    Form for the ExampleValue
    """

    class Meta:
        model = ExampleValue
        fields = ['value']
        widgets = {
            'value': forms.TextInput(
                attrs={'class': "form-control", 'placeholder': 'Optional message'}
            ),
        }


def get_jwt(request):
    cookie_name = 'VouchCookie'
    cookie = request.COOKIES.get('VouchCookie')
    if cookie:
        try:
            validate = requests.get(
                settings.VOUCH_PROXY_VALIDATE_ENDPOINT, cookies={cookie_name: cookie}, verify=False
            )
            validate.raise_for_status()

            # Vouch cookie is URL-safe Base64 encoded Gzipped data
            decompressed = gzip.decompress(base64.urlsafe_b64decode(cookie))
            payload = jwt.decode(decompressed, options={'verify_signature': False})
            return payload
        except Exception as e:
            LOGGER.error("Failed to get JWT: %s", e)
    return None


class IndexView(FormView):
    """
    It's a form with one field, the value to send
    """

    template_name = 'kafka_example/index.html'
    form_class = TestForm
    # When done, redirect back to this page
    success_url = reverse_lazy('example-home')

    def form_valid(self, form):
        """
        The form itself is good, try sending it as a message
        """
        try:
            value = form.cleaned_data.get('value')
            sent = produce_example_message(value)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "Added to queue: %s" % json.dumps(sent),
            )
            LOGGER.debug("Added to queue: %s", sent)
        except Exception as e:
            LOGGER.error(e, exc_info=True)
            messages.add_message(
                self.request,
                messages.ERROR,
                "Uh oh! %s" % e,
            )
        # Those operations set a message in the response
        # but the response itself is always the form looking ok
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add data to the template context
        """
        context = super().get_context_data(**kwargs)
        # Include the last few processed items
        context['recent'] = ExampleValue.objects.order_by('-created_date')[:20]
        context['jwt'] = get_jwt(self.request)
        return context

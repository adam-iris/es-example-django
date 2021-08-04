from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from es_user.lib import get_jwt
from es_user.models import UserJWT
from logging import getLogger

LOGGER = getLogger(__name__)


class UserView(TemplateView):
    """
    Show information about the user
    """

    template_name = 'es_user/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jwt"] = UserJWT.objects.filter(user=self.request.user).first()
        return context


class LoginView(RedirectView):
    """
    Handle login
    """

    def get_redirect_url(self, *args, **kwargs):
        next_page = self.request.GET.get('next_page') or reverse_lazy('user-home')
        if self.request.user.is_authenticated:
            return next_page
        else:
            next_url = self.request.build_absolute_uri(next_page)
            return '/login?url=%s' % next_url


class LogoutView(RedirectView):
    """
    Handle logout, which has a couple components :P
    """

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        next_page = self.request.GET.get('next_page') or reverse_lazy('user-home')
        next_url = self.request.build_absolute_uri(next_page)
        return '/logout?url=%s' % next_url

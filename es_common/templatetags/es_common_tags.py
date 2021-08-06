from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re
from logging import getLogger
from django.utils.encoding import force_text
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlencode
from es_common.utils import safe_json, make_full_url

LOGGER = getLogger(__name__)
register = template.Library()


@register.filter
def keyvalue(d, key):
    """
    Return the value of a key in a dict-like object.

    This is needed when the key value is itself a variable.
    {% for key in ... %}
        The value of "{{ key }}" is {{ d|keyvalue:key }}
    {% endfor %}
    """
    # Check that this is a dict-like object
    if not hasattr(d, '__getitem__'):
        return None
    # Forms expose fields like a dict, but the normal ways to safely access them
    # (ie. get() or __contains__) don't exist so we need to just call and catch KeyError
    try:
        return d[key]
    except KeyError:
        return None


@register.filter(name="range")
def do_range(stop):
    """
    Wrap the standard range() method, to enable things like
    {% for i in range(6) %} ...
    """
    return list(range(stop))


@register.simple_tag
def prevent_auto_submit():
    """
    Include this tag before the <submit> field in a form, and it will prevent the
    form from being submitted if the user hits the Enter key.
    """
    return mark_safe("""
    <!-- Prevent implicit submission of the form -->
    <button type="submit" disabled style="display: none" aria-hidden="true"></button>
    """)


@register.filter
def as_json(value):
    """
    Output the value as JSON
    """
    return safe_json(value, indent=1)


@register.filter
def round_float(value, digits=3):
    """
    Round the float to max digits.

    Django's floatformat is supposed to do this but it doesn't work!
    """
    if value is not None:
        try:
            fvalue = float(value)
            if digits >= 0:
                fvalue = round(fvalue, digits)
            return "%s" % fvalue
        except Exception:
            return value

@register.simple_tag
def full_url(path):
    """
    Return the full URL for the given path (eg. with scheme and domain)
    """
    # Only in production
    if settings.DEBUG:
        return path
    else:
        return make_full_url(path)
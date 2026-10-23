from django import template
from django.template.defaulttags import url as url_tag

register = template.Library()


@register.tag
def url(parser, token):
    """
    Kept so templates using ``{% load url from suit_compat %}`` keep working.
    """
    return url_tag(parser, token)

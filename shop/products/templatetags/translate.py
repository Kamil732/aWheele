from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def translate(text):
    try:
        return _(text)
    except:
        pass
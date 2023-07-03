from django import template

import phonenumbers

register = template.Library()

@register.filter
def get_phonenumber(value):
    return phonenumbers.format_number(value, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
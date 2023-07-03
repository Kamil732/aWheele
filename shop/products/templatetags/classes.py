from django import template
from django.utils.translation import gettext_noop as _

register = template.Library()

@register.filter
def to_class_name(value):
    return _(str(value.__class__.__name__))

@register.simple_tag(takes_context=True)
def is_in_observed_list(context, product):
    observed_list_name = f'observed_{to_class_name(product).lower()}s'
    request = context['request']
    if request.user.is_authenticated:
        observed_list = getattr(request.user, observed_list_name)
        return observed_list.filter(id=product.id).exists()
    else:
        observed_list = request.COOKIES.get(observed_list_name)
        if observed_list:
            observed_list = list(map(int, observed_list.split(',')))
            if product.id in observed_list:
                return True
        return False
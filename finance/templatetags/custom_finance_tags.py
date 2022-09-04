import locale
locale.setlocale(locale.LC_ALL, '')

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
def represent_as_currency(number):
    return locale.currency(int(number), grouping=True, symbol=True)
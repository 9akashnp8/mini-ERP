from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_names: str) -> bool:
    list_of_groups = group_names.split(",")
    return user.groups.filter(name__in=list_of_groups).exists()
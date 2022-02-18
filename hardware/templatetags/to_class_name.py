from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    '''
    _meta.get_field('hardware_id').remote_field.model.__name__
    '''
    
    return value.model.__name__
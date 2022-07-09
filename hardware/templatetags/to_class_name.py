from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    '''
    _meta.get_field('hardware_id').remote_field.model.__name__
    '''
    
    return value.model.__name__

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.simple_tag
def param_replace_2(request, field, value):

    d = request.GET.copy()
    d['page'] = value
    return d.urlencode()
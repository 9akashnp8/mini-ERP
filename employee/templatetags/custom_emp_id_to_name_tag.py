from django import template
from django.template.defaultfilters import stringfilter

from employee.models import Employee


register = template.Library()

@register.filter
def emp_id_to_name(emp_id):
    emp_name = Employee.objects.get(emp_id=emp_id).emp_name
    return emp_name
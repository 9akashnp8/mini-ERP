from django.db.models import (
    QuerySet,
    Count
)
from .models import Laptop

# Business Logic and Helpers

def api_get_laptop_count_by_value(value: str) -> QuerySet:
    """"
    return queryset with count/total objects of each 'value'
    'value' here is a field in the model.

    eg: list of {<value>: <value object>, 'total': <total>}
    """
    queryset = Laptop.objects.values(value).annotate(total=Count('id'))
    return queryset

def get_laptops_assigned(employee_id: str | int) -> QuerySet:
    """
    Returns queryset of laptops assigned to given employee.
    """
    try:
        queryset = Laptop.objects.filter(emp_id=employee_id)
    except ValueError:
        return []
    else:
        return queryset

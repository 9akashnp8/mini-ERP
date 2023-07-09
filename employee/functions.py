from django.db.models import (
    QuerySet,
    Count,
    Q
)

from .models import Employee


def api_get_employee_count_by_value(value: str) -> QuerySet:
    """"
    return queryset with count/total objects of each 'value'
    'value' here is a field in the model.

    eg: list of {<value>: <value object>, 'total': <total>}
    """
    queryset = Employee.objects.values(value).annotate(total=Count('emp_id'))
    return queryset


def api_get_employee_with_without_laptops() -> QuerySet:
    queryset = (
        Employee.objects
        .values('laptop')
        .annotate(
            assigned=Count('emp_id', queryset=Q(laptop__isnull=False)),
            unassigned=Count('emp_id', queryset=Q(laptop__isnull=True))
        )
        .values('assigned', 'unassigned')
    )
    return queryset

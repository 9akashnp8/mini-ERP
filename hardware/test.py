from unittest.mock import Mock
from django.test import TestCase
from django.db.models import QuerySet

from .models import Laptop
from .functions import get_laptops_assigned

class HardwareFunctionTests(TestCase):

    def test_empty_list_returned_for_non_int_emp_id(self):
        m_queryset = Mock(spec=Laptop.objects)
        m_queryset.filter.return_value = m_queryset

        result = get_laptops_assigned("x")

        self.assertEqual(result, [])

    def test_queryset_returned_for_valid_emp_id(self):
        m_queryset = Mock(spec=Laptop.objects)
        m_queryset.filter.return_value = m_queryset

        result = get_laptops_assigned(10)

        self.assertTrue(isinstance(result, QuerySet))

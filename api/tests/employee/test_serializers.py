from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError

from api.serializers import EmployeeCreateSerializer


class EmployeeCreateSerializerTestCase(APITestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.serializer = EmployeeCreateSerializer
        self.data = {
            'emp_email': 'test@example.com',
            'emp_name': 'John Doe',
            'dept_id': 1,
            'desig_id': 1,
            'emp_date_joined': '2023-06-14',
            'emp_phone': '123456789',
            'emp_status': 'Active',
            'lk_emp_id': 'MERP-1',
            'loc_id': 1
        }

    def test_create_employee(self):
        """
        Test successful creation of Employee object and linking of User object.
        """
        serializer = self.serializer(data=self.data)
        if serializer.is_valid(raise_exception=True):
            employee = serializer.save()

        user = User.objects.get(username=self.data['emp_email'])

        self.assertEqual(employee.user, user)
        self.assertEqual(employee.emp_email, self.data['emp_email'])
        self.assertEqual(employee.emp_name, self.data['emp_name'])

    def test_create_employee_existing_user(self):
        """
        Test handling of ValidationError when employee is created with an email
        for which an user already exists.
        """
        User.objects.create_user(
            self.data['emp_email'], self.data['emp_email'], 'merp123'
        )

        serializer = self.serializer(data=self.data)
        if serializer.is_valid(raise_exception=True):
            with self.assertRaises(ValidationError) as context:
                serializer.save()

        expected_error = {
            'emp_email': ['User with username/email already exists']
        }
        self.assertEqual(context.exception.detail, expected_error)

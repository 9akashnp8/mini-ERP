from django.contrib.auth.models import User, Group
from employee.models import Department, Designation, Employee, Location
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from employee.views import *

class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.group = Group(name='admin')
        self.group.save()
        self.user = User.objects.create_user(username='test-user', email='test@test.com', password='test123')
        self.user.groups.add(Group.objects.get(name='admin'))
        self.client.login(username='test-user', password='test123')

class HomePageTest(LoginTestCase):

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_being_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'dashboard.html')

class EmployeeDashboardPageTests(LoginTestCase):

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/employees/")
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        response = self.client.get(reverse('dash_employees'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_being_used(self):
        response = self.client.get(reverse('dash_employees'))
        self.assertTemplateUsed(response, 'employees/employees.html')

class EmployeeDetailPageTests(LoginTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.group = Group.objects.create(name="employee")
        cls.employee = Employee.objects.create(
            lk_emp_id = 'LA-IND-X',
            dept_id = Department.objects.create(dept_name='Test Dept'),
            desig_id = Designation.objects.create(
            dept_id=Department.objects.get(dept_name='Test Dept'), 
            designation="Test Desig"), 
            emp_name = "Akash Test",
            emp_email = "akash.np@lakshyaca.com",
            emp_phone = "8075680388",
            emp_status = "Active",
            loc_id = Location.objects.create(location="Test Location"),
            emp_date_joined = "2022-08-03",
        )

    def test_url_exists_at_correct_location(self):
        url = reverse(employee, args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        url = reverse('employee', args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_being_used(self):
        url = reverse('employee', args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'employees/employee.html')

class EmployeeAddPageTests(LoginTestCase):

    def test_url_exists_at_correct_location(self):
        url = reverse(employee_add_view)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        url = reverse('employee_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_being_used(self):
        url = reverse('employee_add')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'employees/add_new_employee.html')

class EmployeeEditPageTests(LoginTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.group = Group.objects.create(name="employee")
        cls.employee = Employee.objects.create(
            lk_emp_id = 'LA-IND-X',
            dept_id = Department.objects.create(dept_name='Test Dept'),
            desig_id = Designation.objects.create(
            dept_id=Department.objects.get(dept_name='Test Dept'), 
            designation="Test Desig"), 
            emp_name = "Akash Test",
            emp_email = "akash.np@lakshyaca.com",
            emp_phone = "8075680388",
            emp_status = "Active",
            loc_id = Location.objects.create(location="Test Location"),
            emp_date_joined = "2022-08-03",
        )

    def test_url_exists_at_correct_location(self):
        url = reverse(employee_edit_view, args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        url = reverse('employee_edit', args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_being_used(self):
        url = reverse('employee_edit', args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'employees/add_new_employee.html')

class EmployeeDeletePageTests(LoginTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.group = Group.objects.create(name="employee")
        cls.employee = Employee.objects.create(
            lk_emp_id = 'LA-IND-X',
            dept_id = Department.objects.create(dept_name='Test Dept'),
            desig_id = Designation.objects.create(
            dept_id=Department.objects.get(dept_name='Test Dept'), 
            designation="Test Desig"), 
            emp_name = "Akash Test",
            emp_email = "akash.np@lakshyaca.com",
            emp_phone = "8075680388",
            emp_status = "Active",
            loc_id = Location.objects.create(location="Test Location"),
            emp_date_joined = "2022-08-03",
        )

    def test_url_exists_at_correct_location(self):
        url = reverse(employee_delete_view, args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        url = reverse('employee_del', args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_being_used(self):
        url = reverse('employee_del', args=(self.employee.emp_id,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'employees/employee_delete_form.html')

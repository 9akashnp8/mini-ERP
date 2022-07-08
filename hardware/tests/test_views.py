from django.contrib.auth.models import User, Group
from hardware.models import Employee
from django.test import SimpleTestCase, TestCase
from django.test.client import Client
from django.urls import reverse

class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.group = Group(name='admin')
        self.group.save()
        self.user = User.objects.create_user(username='test-user', email='test@test.com', password='test123')
        self.user.groups.add(Group.objects.get(name='admin'))
        self.client.login(username='test-user', password='test123')
    
    def tearDown(self):
        self.user.delete()
        self.group.delete()

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

class OnboardingStep1PageTests(LoginTestCase):

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/onboard/add/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        response = self.client.get(reverse('onbrd_emp_add'))
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_being_used(self):
        response = self.client.get(reverse('onbrd_emp_add'))
        self.assertTemplateUsed(response, 'onboard/onboarding_add_employee.html')

# class OnboardingStep2PageTests(LoginTestCase):

#     def test_url_exists_at_correct_location(self):
#         response = self.client.get(f'/onboard/assign/{self.employee.emp_id}/')
#         self.assertEqual(response.status_code, 200)
    
    # def test_url_available_by_name_and_valid_employee(self):
    #     print(self.user.id)
    #     response = self.client.get(reverse('onbrd_hw_assign', args=[182]))
    #     self.assertEqual(response.status_code, 200)
    
    # def test_url_available_by_name_with_invalid_employee(self):
    #     pass
    
    # def test_correct_template_being_used(self):
    #     response = self.client.get(reverse('onbrd_hw_assign', args=[182]))
    #     self.assertTemplateUsed(response, 'onboard/onboarding_assign_hardware.html')

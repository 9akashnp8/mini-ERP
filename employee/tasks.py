from celery import shared_task
from environs import Env
from datetime import datetime

from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail

from employee.models import Employee
from hardware.models import Laptop

env = Env()
env.read_env()

@shared_task
def employee_add_email(emp_id):
    employee_info = Employee.objects.get(emp_id=emp_id)
    URL = f"https://erp.lakshyaca.com/{reverse('onbrd_hw_assign', args=(emp_id,))}"
    SUBJECT = f"[miniERP] New Employee Added: {employee_info.emp_name}"
    context = {
        'emp_name': employee_info.emp_name,
        'url': URL,
        'lk_emp_id': employee_info.lk_emp_id,
        'dept_id': employee_info.dept_id,
        'desig_id': employee_info.desig_id,
        'loc_id': employee_info.loc_id
    }
    MESSAGE = render_to_string('employee/employee_add_email.html', context)
    FROM = 'notifications.miniERP@gmail.com'
    send_mail(SUBJECT, MESSAGE, FROM, env.list("EMAIL_RECIPIENTS"), fail_silently=True, html_message=MESSAGE)

@shared_task
def employee_exit_email(emp_id, laptop_id):
    employee_info = Employee.objects.get(emp_id=emp_id)
    laptop_info = Laptop.objects.get(id=laptop_id)
    SUBJECT = f"[miniERP] Employee Exit Complete: {employee_info.emp_name}"
    context = {
        'emp_name': employee_info.emp_name,
        'lk_emp_id': employee_info.lk_emp_id,
        'dept_id': employee_info.dept_id,
        'desig_id': employee_info.desig_id,
        'loc_id': employee_info.loc_id,
        'laptop_hardware_id': laptop_info.hardware_id,
        'laptop_serial_number': laptop_info.laptop_sr_no,
        'dated': datetime.today()
    }
    MESSAGE = render_to_string('employee/employee_exit_email.html', context)
    FROM = 'notifications.miniERP@gmail.com'
    send_mail(SUBJECT, MESSAGE, FROM, env.list("EMAIL_RECIPIENTS"), fail_silently=True, html_message=MESSAGE)
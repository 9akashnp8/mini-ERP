from datetime import datetime
from celery import shared_task
from environs import Env

from django.core.mail import send_mail
from django.template.loader import render_to_string

from hardware.models import Laptop

env = Env()
env.read_env()

# Tasks
@shared_task
def laptop_assigned_notif(emp_id, emp_name, laptop_hardware_id, laptop_serial_number, laptop_processor, laptop_screen_size, laptop_remarks):
    SUBJECT = f"[miniERP - Laptop Assigned] {laptop_serial_number} has been assigned to {emp_name}."
    context = {
        'email_heading': f'Laptop [{laptop_serial_number}] has successfuly been assigned to {emp_name} | {emp_id}',
        'emp_id': emp_id,
        'emp_name': emp_name,
        'laptop_hardware_id': laptop_hardware_id,
        'laptop_serial_number': laptop_serial_number,
        'laptop_processor': laptop_processor,
        'laptop_screen_size': laptop_screen_size,
        'laptop_remarks': laptop_remarks,
        'dated': datetime.today()
    }
    MESSAGE = render_to_string('hardware/laptops/laptop_assign_return_replace_notif_mail.html', context)
    FROM = 'notification.minierp@gmail.com'
    send_mail(SUBJECT, MESSAGE, FROM, env.list("EMAIL_RECIPIENTS"), fail_silently=True, html_message=MESSAGE)

@shared_task
def laptop_returned_notif(emp_id, emp_name, laptop_hardware_id, laptop_serial_number, laptop_processor, laptop_screen_size, laptop_remarks):
    SUBJECT = f"[miniERP - Laptop Returned] {laptop_serial_number} has been returned by {emp_name}."
    context = {
        'email_heading': f'Laptop [{laptop_serial_number}] has been returned by {emp_name} | {emp_id}',
        'emp_id': emp_id,
        'emp_name': emp_name,
        'laptop_hardware_id': laptop_hardware_id,
        'laptop_serial_number': laptop_serial_number,
        'laptop_processor': laptop_processor,
        'laptop_screen_size': laptop_screen_size,
        'laptop_remarks': laptop_remarks,
        'dated': datetime.today()
    }
    MESSAGE = render_to_string('hardware/laptops/laptop_assign_return_replace_notif_mail.html', context)
    FROM = 'notification.minierp@gmail.com'
    send_mail(SUBJECT, MESSAGE, FROM, env.list("EMAIL_RECIPIENTS"), fail_silently=True, html_message=MESSAGE)

@shared_task
def laptop_add_notif(laptop_id):
    laptop_info = Laptop.objects.get(id=laptop_id)
    SUBJECT = f"[miniERP - Laptop Added] {laptop_info.laptop_sr_no} has been added to the database."
    context = {
        'email_heading': f'Laptop [{laptop_info.laptop_sr_no} | {laptop_info.hardware_id}] has been added to the database.',
        'laptop_hardware_id': laptop_info.hardware_id,
        'laptop_serial_number': laptop_info.laptop_sr_no,
        'laptop_processor': laptop_info.processor,
        'laptop_screen_size': laptop_info.screen_size,
        'laptop_remarks': laptop_info.laptop_return_remarks,
        'dated': datetime.today()
    }
    MESSAGE = render_to_string('hardware/laptops/laptop_add_mail.html', context)
    FROM = 'notification.minierp@gmail.com'
    send_mail(SUBJECT, MESSAGE, FROM, env.list("EMAIL_RECIPIENTS"), fail_silently=True, html_message=MESSAGE)

    
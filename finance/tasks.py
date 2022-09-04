import datetime
from celery import shared_task
from environs import Env

from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string

from finance.models import Payment, Service

env = Env()
env.read_env()

# Helpers
def add_months(input_date, months_to_add):
    from dateutil.relativedelta import relativedelta
    months_added_date = input_date + relativedelta(months=months_to_add)
    return months_added_date

today = datetime.date.today()

SITE_DOMAIN = 'http://127.0.0.1:8000'

# Tasks
@shared_task
def auto_update_next_due_date():
    """
    +1 Month/Quater/Year for Service Due dates
    """
    active_services = Service.objects.filter(status="Active")

    for service in active_services:
        if service.estimated_due_date == today:
            if service.payment_interval == "M":
                service.estimated_due_date = add_months(service.estimated_due_date, 1)
                service.save()
            elif service.payment_interval == "Q":
                service.estimated_due_date = add_months(service.estimated_due_date, 3)
                service.save()
            elif service.payment_interval == "H":
                service.estimated_due_date = add_months(service.estimated_due_date, 6)
                service.save()
            elif service.payment_interval == "Y":
                service.estimated_due_date = add_months(service.estimated_due_date, 12)
                service.save()
            else:
                print("Payment Interval is OT, Next Due Date not required.")
        else:
            pass

@shared_task
def due_date_reminders():
    """
    Reminder on due date.
    """
    active_services = Service.objects.filter(status="Active")

    for service in active_services:
        if service.estimated_due_date == today:
            SUBJECT = f"[miniERP] Payment for {service.platform} is Due Today"
            context = {
                'platform': service.platform,
                'current_cost': service.current_cost,
                'payment_update_url': f"{SITE_DOMAIN}{reverse('service_payments', args=[service.id])}"
            }
            MESSAGE = render_to_string('finance/service_due_date_reminder.html', context)
            FROM = 'notifications.miniERP@gmail.com'
            send_mail(SUBJECT, MESSAGE, FROM, env.list("EMAIL_RECIPIENTS"), fail_silently=True, html_message=MESSAGE)

@shared_task
def auto_add_payment():
    """
    auto create a "pending" payment transaction on due date.
    """
    active_services = Service.objects.filter(status="Active")
    
    for service in active_services:
        if service.estimated_due_date == today:
            payment_for_service = Payment.objects.create(
                service = service,
                payment_for_month = datetime.date(today.year, today.month, 1),
                payment_status = "Pending",
                amount = service.current_cost
            )

@shared_task
def payment_mail(payment_id):
    payment_obj = Payment.objects.get(id=payment_id) 
    SUBJECT = f"[miniERP] IT Expense for {payment_obj.payment_for_month.strftime('%B')} - {payment_obj.service}"      
    context = {
        'service': payment_obj.service,
        'payment_for_month': payment_obj.payment_for_month,
        'amount': payment_obj.amount,
        'invoice_no': payment_obj.invoice_no,
        'card_no': payment_obj.card_no
    }
    MESSAGE = render_to_string('finance/payment_mail.html', context)
    FROM = 'notifications.miniERP@gmail.com'
    send_mail(SUBJECT, MESSAGE, FROM, env.list("EMAIL_RECIPIENTS"), fail_silently=True, html_message=MESSAGE)
    
    
            




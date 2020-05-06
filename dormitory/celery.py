"""
celery tasks and settings.
"""
from sendgrid.helpers.mail import *
import os
from celery import Celery
from sendgrid import SendGridAPIClient

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dormitory.settings')

celery_app = Celery('dormitory')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


@celery_app.task()
def debug_task():
    for x in range(100):
        print(x)


@celery_app.task(default_retry_delay=300, max_retries=5)
def send_email_registration(email, password):
    message = Mail(
        from_email='',
        to_emails=email,
        subject='Dormitory registation',
        html_content=f"<strong> hello, it's your password:{password}</strong>")
    try:
        sg = SendGridAPIClient('')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))


@celery_app.task(default_retry_delay=300, max_retries=5)
def send_email_room(email, room):
    message = Mail(
        from_email='',
        to_emails=email,
        subject='Dormitory change room',
        html_content=f"<strong> hello you changed room:{room}</strong>")
    try:
        sg = SendGridAPIClient('')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

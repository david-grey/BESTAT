# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from django.core.mail import send_mail

@shared_task()
def test(text):
    print('start send email to %s' % text)
    time.sleep(5)
    print('success')
    return True


@shared_task()
def emailto(email_body,user_email):
    send_mail(subject="Verify your email address",
                  message=email_body,
                  from_email="bestat.verify@gmail.com",
                  recipient_list=[user_email])
    print('success')
    return True

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from celery import shared_task

        
@shared_task
def send_otp_email(email, username, otp_link):
    subject = ('OTP')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    context = {
        'username' : username,
        'url' : otp_link, 
        'admin_email': settings.ADMIN_EMAIL}
    
    html_email = render_to_string('./template/emails/send_otp.html', context=context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)   
    
    try:
        email.send()
    except Exception as err:
        print(err)
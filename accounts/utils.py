from uuid import uuid4
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from .models import User

def sendVerificationMail(request):
    user = request.user
    token =  uuid4()
    user.email_token = token
    user.save()
    subject = 'Welcome to OnePanel System'
    message = f'Hi!\n{user.name}, thank you for registering in OnePanel System.\nPlease Click here to verfy Your Account {Site.objects.get_current().domain}/accounts/email-verification/{user.id}/{token}/\nThis is a Computer generated mail don\'t reply to this mail'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )

def sendPasswordResetMail(request):
    user = User.objects.get(email = request.data.get('email'))
    subject = 'Password Reset Mail'
    uuid = uuid4()
    user.password_reset_token = uuid
    user.save()
    message = f'Click here to reset password : {Site.objects.get_current().domain}/accounts/password-reset-redirect/{user.id}/{uuid}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )
from django.contrib.auth.models import User 
from django.core.mail import send_mail


def get_vertification():
    return "The Link"


def send_vertification_email(email_addr):

    message="Welcome\nPlease active your account by clicking on the link below\n"
    send_mail(
        'Please activate your account ',
         message,
         None,#Taken from default_from_email in settings.py
        [email_addr],
        fail_silently=False



    )
    #print("The email address is " , email_addr)

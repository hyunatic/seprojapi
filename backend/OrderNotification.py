#this entire file is the one that will handle the verfication of account
#But may not work depend on your host configuration 

# ****** NOTED ******************************************
#since the backend is not doing much other than handle REST api call to CRUD the database
#I can just dump most of the thing here for easily maintenance and portabitly

from django.contrib.auth.models import User
from .models import Post,Order
from django.views import View
from django.core.mail import send_mail


# When an Order had been make 
def send_OrderMake_email( req_username ,postarg):
    #get the domain name of where our website store at 
    
    postobj = Post.objects.get(pk=postarg)
    
    userobj = postobj.Userid
    

    message="Hi " + userobj.username +"\n"+ req_username + " had request the following item  from you.\n\n\t"+ postobj.ItemName  +"\n\nPlase Login in to our website to accept the order."
    send_mail(
        'Request Item awaiting your approval! ',
         message,
         None,  #derived from default_from_email in settings.py
        [userobj.email],
        fail_silently=False

    )


def send_OrderOutcome(usercode ,OID,outcome):
    
    userobj = User.objects.get(username=usercode)
   
    
    message="Hi " + userobj.username +"\n" +"This is to inform you that your Order ID " + str(OID) + " had been " + outcome +  ".\n Regards"
    send_mail(
        'Your Order had been ' + outcome +'!',
         message,
         None,  #derived from default_from_email in settings.py
        [userobj.email],
        fail_silently=False

    )


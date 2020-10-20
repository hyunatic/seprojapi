#this entire file is the one that will handle the verfication of account
#But may not work depend on your host configuration 

# ****** NOTED ******************************************
#since the backend is not doing much other than handle REST api call to CRUD the database
#I can just dump most of the thing here for easily maintenance and portabitly

from django.contrib.auth.models import User 
from django.views import View
from django.core.mail import send_mail


#import django library to do the encoding and redirect 
from django.shortcuts import  redirect
from django.http import HttpResponse
# Library need to encode the URL and activate user 
from django.urls import  reverse
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type




# REF: 
# https://www.youtube.com/watch?v=e3UhXKVECPI and the next video In the series 


#Noted that if the backend project scope is extend such as to include the forget password functionatly This will need to put in another 
#python file call util.py to prevent duplicated of code

# this token or /link it use to ensure that the user don`t use the samelink to access the website
#text type ensure it compatible
class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

token_generator = AppTokenGenerator()
# the view that reflect Since ny view.py is the one handle the python call I can just leave it here 
class VertificationView(View): 
    def get(self,request,uidb64,token):
        try:
            #decode the UID from the URL since it not shown in plain text 
            userid = force_text(urlsafe_base64_decode(uidb64))
            user =User.objects.get(pk=userid)

            if not token_generator.check_token(user,token):
                html="<html><head> <title>  Oh no </title> </head> <body> <h1> Account already been activated</h1>  </body> </html>"
                return HttpResponse(html)

            if(user.is_active ==False):
                user.is_active=True
                user.save()
                
                html="<html><head> <title>  Success </title> </head> <body> <h1> Success</h1>  </body> </html>"
                return HttpResponse(html)
            else:
                #Another fail safe just Incase the first if statement pass but the account is activate
                #You can redirect to the fron`t end
                return  redirect("http://www.github.com")
        except Exception as ex:
            print(str(ex))


     

#get the link
def get_vertification_link(userobj):
    #encode the UID
    uidb64 = urlsafe_base64_encode(force_bytes(userobj.pk))
    
    
    #AMMEND THIS set your domain Since it a helper method there is no request 
    domain = "localhost:8000"


    link=reverse('activate',kwargs={'uidb64':uidb64 ,'token':  token_generator.make_token(userobj)})
    return "http://"+domain+link



def send_vertification_email( useremail):
    #get the domain name of where our website store at 
    userobj = User.objects.get(email=useremail)
    link =get_vertification_link(userobj)
    
    message="Welcome " + userobj.username  +"\nPlease active your account by clicking on the link below\n"  
    message += link
    send_mail(
        'Please activate your account ',
         message,
         None,  #derived from default_from_email in settings.py
        [userobj.email],
        fail_silently=False



    )
    #print("The email address is " , email_addr)
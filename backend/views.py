# THIS WHERE THE API CALLED HAPPEN

#Import Django Library
from django.shortcuts import render ,redirect
from django.http import HttpResponse, Http404,JsonResponse
from django.utils.http import is_safe_url

from django.contrib.auth.models import User 
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings  #Import your setting from Django

#User.object.get()


#Import the rest-frame work Library
from rest_framework.authentication import SessionAuthentication
from  rest_framework.response import Response
from  rest_framework.decorators import api_view ,authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

#Import the backend data  

from .email import send_vertification_email


from .serializer import CreateUserSerailizer
from  .serializer import LoginUserSeralizer


#USE THIS TO ALLOW ONLY CERTAIN HOST  TO CALL THE APP define in SE_master.py
ALLOWED_HOST = settings.ALLOWED_HOSTS

#Administrator password is Unwanted1
#user1 password is         Unwanted2


#Login APi the URL is at url.py 
#Check the login get data via the URL
@api_view(['POST'] )
def login(request,*args,**kwargs):
    
    Login_user_seralizer = LoginUserSeralizer(data=request.data)

    usercode =Login_user_seralizer.get_username(request.data)
    passcode = Login_user_seralizer.get_password(request.data)

    resultvalue = Login_user_seralizer.checkauthentication(usercode,passcode)
    data={
            "Result": resultvalue
     }
    return Response(data, status=200) 


# API to create user 

#Format to follow : CASE SENSETIVE
# {
# 	"username": "user2",
# 	"password": "123",
# 	"email": "2@2.com"
# }

#1= Sucess  0= Failure in REST/Serializer  -1= Email
# HELPER METHOD usually it put on seperate File but Since only have 2 method I just leave it here 

def check_userExist( userCode):
    try:
        User.objects.get(username=userCode)
        #result found should not create the user 
        return 1
    except ObjectDoesNotExist:

        return 0

def check_emailExist(emailCode):
    try:
        User.objects.get(email=emailCode)
        #result found should not create the user 
        return 1
    except ObjectDoesNotExist:

         return 0

# Call this the above 2 are just helper method
#get data via JSON 
@api_view(['POST'] )
def create_User(request,*args,**kwargs):
#ss
    create_user_seralizer = CreateUserSerailizer(data=request.data)
    #Now come the hard part of sending the request.data into here

    usercode = create_user_seralizer.getUsername(request.data)
    emailcode = create_user_seralizer.getEmail(request.data)

    if check_emailExist(emailcode) == 1 :
        data={
            "Result": "Email already exist"
        }
        return Response(data,status=500)


    if  check_userExist(usercode) == 1: 
        data={
            "Result": "Username  already exist"
            
        }
        return Response(data,status=500)
    else :
        #IGNORE THE RED LINE if any 
        if create_user_seralizer.is_valid(raise_exception=True):
        #create_user_seralizer.save(is_active='False')
            create_user_seralizer.create(request.data)
            data= {
            "Result": 1
            }
            try:
                send_vertification_email(emailcode) 
                return Response(data, status=200) 
            except:
                #if email FAILED For some funny reason 
                return Response({"Result": -1}, status=500) 

        return Response({"Result": 0}, status=500) 


#-----------------------------------------  CRUD Product Table-------------------------------------------------








#-------------------------------REFERENCE CODE-------------------------------------------------------------------
# @api_view(['GET'])
# #This will throw an error if user is not authenticated 
# #@authentication_classes(['SessionAuthentication'])
# #@permission_classes([IsAuthenticated])
# def list_view(request,*args  ,**kwargs):
#     qs = Tweet.objects.all()
    
#     seralizer = TweetSerializer(qs, many=True)

   
#     return Response(seralizer.data ,status=200)



# @api_view(['GET'])
# def single_tweet_view(request, tweet_id ,*args ,**kwargs):

#     qs = Tweet.objects.filter(id= tweet_id)

#     if not qs.exists: 
#         print("This is a test ")
#         return Response({} ,status=404)

#     obj = qs.first()
#     if obj == None: 
#         return Response({} ,status=404)
        
#     seralizer = TweetSerializer(obj)
#     return Response(seralizer.data ,status=200)




# #this method only support POST  and must authenticated
# #WE CAN USE CLASS BASED VIEW TO help prevent repeating code 
# @api_view(['POST'])
# def create_tweet_view(request ,*args ,**kwargs):

#     serializer = TweetSerializer(data=request.POST)

#     #send back what the error is before
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(user=request.user)
#         return Response(serializer.data, status=201)

#     return Response({},status =400)




# #THE MAINPAGE
# def home_view(request, *args,**kwargs):
#     #return HttpResponse("<h1> This is just a basic view for HTML</h1>")
#     return render(request,'public/index.html',context={},status=200)

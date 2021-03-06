# THIS WHERE THE API CALLED HAPPEN

#Import Django Library Some are kept just in case I need to use it 
from django.shortcuts import render ,redirect
from django.http import HttpResponse,JsonResponse


from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings  #Import your setting from Django


#Import the rest-frame work Library
from  rest_framework.response import Response
#One of them is for mine class based view
from  rest_framework.decorators import api_view  
from rest_framework.views import APIView



from .Verifyaccount import send_vertification_email
from .serializer import CreateUserSerailizer
from .serializer import LoginUserSeralizer
from .serializer import SuccessLoginSeralizer



from .serializer import PostItemSeralizer
from .serializer import UpdateItemSeralizer
from .serializer import DeleteItemSeralizer
from .serializer import get_SearchdetailSeralizer
from .serializer import SearchItemSeralizer
from .serializer import get_detailViewUserItemSeralizer
from .serializer import ViewItemSeralizer


from .serializer import MakeOrderSeralizer
from .serializer import get_usernameserializer
from .serializer import View_SenderOrderSeralizer
from .serializer import View_reqOrderSeralizer
from .serializer import Approve_Disapprove_OrderSeralizer
from .serializer import DeleteOrderSeralizer


from .models import Post ,Order ,Profile
from django.contrib.auth.models import User 
from django.db.models import Q  # For Query
from .Verifyaccount import send_vertification_email;
from .OrderNotification import send_OrderMake_email ,send_OrderOutcome


#  List of the dummy account.
#Administrator password is Unwanted1
#user2 password is         Unwanted2
#user3 password is         Unwanted3

#If not mention 0 mean API failed 1 mean API Pass 


# the URL is at url.py 


#Login APi 
#Check the login get data via the URL
#0= login fail  1=Pass
#JSON Syntax 
# {
#    "username":"user2",
#    "password":"Unwanted2"
# }
@api_view(['POST'] )
def login(request,*args,   **kwargs):
    
    Login_user_seralizer = LoginUserSeralizer()

    usercode =Login_user_seralizer.get_username(request.data)
    passcode = Login_user_seralizer.get_password(request.data)

    resultvalue = Login_user_seralizer.checkauthentication(usercode,passcode)
    
    if(resultvalue == 1 ):

        qs = User.objects.get(username=usercode)
        seralizer = SuccessLoginSeralizer(qs)
        return Response(seralizer.data ,status=200)
    
    
    data={
            "Result": resultvalue
     }
    return Response(data, status=200) 




# API to create user 

#Format to follow : CASE SENSETIVE
# {
# 	"username": "user2",
# 	"password": "123",
# 	"email": "2@2.com",
#   "Hall": " "
# }

#1= Sucess  0= Failure in REST/Serializer  -1= Email Failure
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
            create_user_seralizer.createUser(request.data)
            data= {
            "Result": 1
            }
            #send_vertification_email(emailcode) 
            try:
                send_vertification_email(emailcode) 
                return Response(data, status=200) 
            except:
                #if email FAILED For some funny reason 
                return Response({"Result": -1}, status=500) 

        return Response({"Result": 0}, status=500) 



#To -resend the verficaation code back to the User       
# {
# 	"username": "user2",
#}
#If success I will return 1 else I will state the error message
@api_view(['POST'] )
def re_sendVerification(request,*args,**kwargs):
    try:
        get_username_serializer = get_usernameserializer()
        usercode = get_username_serializer.getUsername(request.data)
        userobj = User.objects.get(username=usercode)
        send_vertification_email(userobj.email)
        return Response({"Result": 1}, status=200) 

    except ObjectDoesNotExist:

        data={
            "Result": "No existing account with that username had been registerd in our record, Please re-create"
        }

        return Response(data,status=404)


#JSON FORMAT
#Format to follow : CASE SENSETIVE
# {
# 	"username": "user2",
# 	"password": "123",
# 	"email": "2@2.com",
#   "Hall": " "
# }
@api_view(['POST'] )
def update_Profile(request,*args,**kwargs):
    create_user_seralizer = CreateUserSerailizer(data=request.data)

 
        #create_user_seralizer.save(is_active='False')
    resultvalue = create_user_seralizer.updateprofile(request.data)
    data= {
            "Result": resultvalue
    }

    return Response(data,status=404)



#-----------------------------------------  CRUD Post  Table-------------------------------------------------

@api_view(['GET'])
def list_view(request,*args ,**kwargs):
    #Do not get the Administrator Post Item  

    order_confirm = Order.objects.filter(OrderConfirm=1).values_list('Postid_id')
    qs = Post.objects.filter(~Q(pk__in = order_confirm))
    #Another way
    #qs = Post.objects.all().order_by('Userid')
    seralizer = SearchItemSeralizer(qs,many=True)
    

    return Response(seralizer.data ,status=200)


#List the post belong to the User
#JSON Format for list_userview
# {
#     "username": "user2"
# }
@api_view(['POST'])
def list_user_view(request ,*args ,**kwargs):


    list_user_seralizer = get_detailViewUserItemSeralizer(data=request.data)
    qs=None 

    userarg = list_user_seralizer.getusername(request.data)
    userobj = User.objects.filter(username=userarg)
    qs = Post.objects.filter( Q(Userid__in = userobj)  ).order_by("PostDate")


    #set Many to true to return many value
    seralizer = ViewItemSeralizer(qs, many=True)
    return Response(seralizer.data ,status=200)


#Another way to define .. this is call class based vieW
#JSON format
# {
# "searchType": "ItemName/Category/Hall",
# "searchArg" : "XXXXXX",
#"searchOrd": "ASC,DESC"
# }
#ASC=  Oldest First #DESC is latest 
class search_post_Item(APIView ):
    #if the API is a POST request
    def post(self,request,format=None):
        search_post_item_seralizer = get_SearchdetailSeralizer()

        searchType = search_post_item_seralizer.getSearchType(request.data)
        searchArg = search_post_item_seralizer.getSearchArg(request.data)
        searchOrder = search_post_item_seralizer.getSearchOrder(request.data)
        order_confirm = Order.objects.filter(OrderConfirm=1).values_list('Postid_id')
        qs= None

        if searchOrder == "ASC":
             if searchType=="ItemName":
                    qs=Post.objects.filter(Q(ItemName__icontains=searchArg) &  ~Q(pk__in = order_confirm) ).order_by("PostDate")
                    seralizer =SearchItemSeralizer(qs,many=True)
                    return Response(seralizer.data ,status=200)
             elif  searchType =="Category":
                    qs =Post.objects.filter( Q(Category__iexact=searchArg) & ~Q(pk__in = order_confirm)).order_by("PostDate")
                    seralizer =SearchItemSeralizer(qs,many=True)
                    return Response(seralizer.data ,status=200)
             elif searchType =="Hall":
                    #Hallobj = Profile.objects.get(Hall=searchArg)
                    inthat_hall = Profile.objects.filter(Hall=searchArg).values_list('Userid_id')
                    qs=Post.objects.filter(  Q(Userid__in = inthat_hall) &  ~Q(pk__in = order_confirm)  ).order_by("PostDate")
                    seralizer=SearchItemSeralizer(qs,many=True)
                    return Response(seralizer.data ,status=200)
                 
        elif searchOrder == "DESC" :
             if searchType=="ItemName":
                    qs=Post.objects.filter(Q(ItemName__icontains=searchArg) &  ~Q(pk__in = order_confirm)).order_by("-PostDate")
                    seralizer =SearchItemSeralizer(qs,many=True)
                    return Response(seralizer.data ,status=200)
             elif  searchType =="Category":
                    qs =Post.objects.filter(Q(Category__iexact=searchArg) & ~Q(pk__in = order_confirm)).order_by("-PostDate") 
                    seralizer =SearchItemSeralizer(qs,many=True)
                    return Response(seralizer.data ,status=200)
             elif searchType =="Hall":
                    #Hallobj = Profile.objects.get(Hall=searchArg)
                  
                    inthat_hall = Profile.objects.filter(Hall=searchArg).values_list('Userid_id')
                    qs=Post.objects.filter(  Q(Userid__in = inthat_hall) &  ~Q(pk__in = order_confirm)  ).order_by("-PostDate")
                    seralizer=SearchItemSeralizer(qs,many=True)
                    return Response(seralizer.data ,status=200)


        return Response({"Result": -1}, status=500) 
        


  


    def get(self,request,format=None):
        return Response({"Result": -1}, status=500) 



#JSON format to POST Item
#postid is the an auto generated the POST Number
#Due to the model of Post and aut_user had a Many to  1 relation 
#the model.seralizer need an User instance in that the case just pass in 1 which is the UID of the administrator
#  {
#    "Userid":1,
#    "username": "user2",
#    "ItemName":"Apple2",
#    "Category":"Iphone",
#    "Description":"NOT 4 SALE",
#    "PostDate":"2020-10-10",
#    "ImageId": "Apple"
#   }

@api_view(['POST','GET'] )
def postItem(request,*args, **kwargs):
    create_post_seralizer = PostItemSeralizer(data=request.data)

    if create_post_seralizer.is_valid(raise_exception=True):
        #create_user_seralizer.save(is_active='False')
        result_value=create_post_seralizer.CreatePost(request.data)

        data= {
        "Result": result_value
        }
    return Response(data, status=200) 


#JSON SYNTAX
# Format is YYY-MM-DD
# {
#   "Postid": 3,
#   "ItemName": "Apple20",
#   "Description": "PLEASE TAKE",
#   "PostDate": "2025-12-01"
# }

@api_view(['POST'] )
def updateItem(request,*args, **kwargs):
    
    update_item_seralizer = UpdateItemSeralizer(data=request.data)

    if(update_item_seralizer.is_valid(raise_exception=True)):
        
        result_value = update_item_seralizer.updatePost(request.data)
        data= {
        "Result": result_value
        }
    
    return Response(data, status=200) 




#use this with list_user_view

#JSON FORMAT
#{
#    "Postid" : 6
#}

@api_view(['POST','GET'] )
def deleteItem(request,*args, **kwargs):
    Delete_post_seralizer = DeleteItemSeralizer()
    resultvalue = Delete_post_seralizer.DeletePost(request.data)
 
    
    data= {
    "Result": resultvalue
    }
    return Response(data, status=200) 




#-------------------------------------------CRUD Order table -------------------------------
#JSON format to POST Item same as it is ref to user object you will need req_Userid
#Userid just leave it 1 

#Date format is YYYY-MM-DD"
#Time hr:mm
#movingService True or False
#req_username refer to the USER THAT IS REQUESTING THE ITEM

#JSON FORMAT

#  {
#     "Postid":"8",
#     "req_Userid":"1",
#     "req_username": "user3",
#     "Date":"2020-10-10",
#     "Time":"20:20",
#     "Location":"Sing",
#     "MovingService":"False"
#  }
@api_view(['POST'] )
def makeOrder(request,*args, **kwargs):

    create_order_seralizer = MakeOrderSeralizer(data=request.data)

    requsercode = create_order_seralizer.getUsername(request.data)
    postcode = create_order_seralizer.getPostid(request.data)

    if create_order_seralizer.is_valid(raise_exception=True):
        
        #create_user_seralizer.save(is_active='False')
        
        
        result_value= create_order_seralizer.makeOrder(request.data)
        data= {
        "Result": result_value
        }

        if(result_value ==1):
            try:
                send_OrderMake_email(requsercode,postcode) 
            except:
                #if email FAILED For some funny reason 
                return Response({"Result": -1}, status=500) 
           


        return Response(data, status=200) 




#This method will list all order that await the user to approve
# user2 refer to the order wait User2 to approve

#JSON FORMAT
# {
# "username": "user2"
# }
@api_view(['POST'] )
def listOrder_2approve(request,*args,**kwargs):

    #get the username out of JSON
    get_username_serializer = get_usernameserializer()
    usercode = get_username_serializer.getUsername(request.data)


    #get the user objectname
    userobject = User.objects.get(username=usercode)


    #get thoose postID that belong to this user
    user_post = Post.objects.filter(Userid=userobject.pk).values_list('Postid')


    #Filter out thoose order make by this user
    qs =Order.objects.filter( Q (Postid__in = user_post) )

    seralizer = View_SenderOrderSeralizer(qs,many=True)
    

    return Response(seralizer.data ,status=200)



#This method will handle approve or Disapprove 
# 1 = Approve 0 = ERROR  -1 = Disapprove Order will be delete and email will be send 
#JSON FORMAT
# {

# "OrderId": "X",
# "OrderConfirm": True/False

# }

@api_view(['POST'] )
def order_decision(request,*args,**kwargs):

    order_desc_serializer = Approve_Disapprove_OrderSeralizer()

    #get the descsion and the orderID
    decision = order_desc_serializer.getdecision(request.data)
    orderid = order_desc_serializer.getorderID(request.data)

    #get the order object so we can get the user object ( Using it to send email notifiation)
    orderobj = Order.objects.get(pk=orderid)
    usercode = orderobj.req_Userid.username

    result_value = order_desc_serializer.implementdecision(request.data ,decision)
    outcome= "Approved"
    data= {
        "Result": result_value
    }


    if(result_value == -1):
        outcome= "Refused"

    elif (result_value == 0):
         return Response(data, status=200) 
    elif (result_value == 1):
        #Delete and send rejection letter for those order who had request the same item but that item is 
        #Is approve on another order
        postobj = orderobj.Postid 
        rejectOrder = Order.objects.filter( ~Q(pk=orderid)   & Q(Postid=postobj) )

        for x in rejectOrder:
            print(x.req_Userid.username)
            send_OrderOutcome(x.req_Userid.username,x.pk,"Refused")
            x.delete()


    
    send_OrderOutcome(usercode,orderid,outcome)
    return Response(data, status=200) 


#Get all order make by you
#JSON FORMAT
# {
# "username": "user2"
# }
@api_view(['POST'] )
def listOrder_makebyU(request,*args,**kwargs):

    #get the username out of JSON
    get_username_serializer = get_usernameserializer()
    requserCode = get_username_serializer.getUsername(request.data)


    #get the user objectname
    userobject = User.objects.get(username=requserCode)

    #Filter out thoose order make by the user
    qs =Order.objects.filter( req_Userid=userobject.pk)

    seralizer = View_reqOrderSeralizer(qs,many=True)
    

    return Response(seralizer.data ,status=200)


#JSON FORMAT
# {
# "OrderId": X
# }
@api_view(['POST'] )
def deleteOrder(request,*args, **kwargs):

    Delete_order_seralizer = DeleteOrderSeralizer()
    resultvalue = Delete_order_seralizer.DeleteOrder(request.data)
 
    
    data= {
    "Result": resultvalue
    }
    return Response(data, status=200) 



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

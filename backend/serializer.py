from django.conf import  settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import Post,Order,Profile


#Model serializer allow us to use the existing model in model.py
# So we no need to type out all the field


#Writing and Delete to the database is done here 



#On the contary I can just Create 1 big seralizer ??
#But I prefer to make it independent such that each searlizer do certain task 

class PostItemSeralizer(serializers.ModelSerializer):
    class Meta:
        model =Post
        fields='__all__'
        #Need see how to picture it 
        #'__all__'
    
    def CreatePost(self,validated_data):
        userobj = User.objects.get(username=validated_data['username'])
        #profileobj =Profile.objects.get(Userid=userobj.pk)
        #print(uid)
        postobj = Post( Userid=userobj ,ItemName=validated_data['ItemName'],Category=validated_data['Category'],Description=validated_data['Description'],PostDate=validated_data['PostDate'],ImageId=validated_data['ImageId'])
        postobj.save()
        
        try:
            postobj.save()
            return 1
        except:
            return 0
   
class DeleteItemSeralizer(serializers.ModelSerializer):
    class Meta:
        model =Post
        fields=('Postid')


    def DeletePost(self,validated_data):
        try:
            postobj = Post.objects.get(pk=validated_data['Postid'])
            postobj.delete() 
            return 1
        except:
            return 0 


class UpdateItemSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields=('Postid','ItemName','Description','PostDate')
    
    def updatePost(Self,validated_data):
        postobj= Post.objects.get(pk=validated_data['Postid'])

        postobj.ItemName = validated_data['ItemName']
        postobj.Description = validated_data['Description']
        postobj.PostDate = validated_data['PostDate']
        postobj.save()
        return 1 




class get_detailViewUserItemSeralizer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username']
    def getusername(self,vaildatedata):
        return vaildatedata['username']


class ViewItemSeralizer(serializers.ModelSerializer):
    Username = serializers.SerializerMethodField('get_username',read_only=True)
    Email = serializers.SerializerMethodField('get_email',read_only=True)
    Hall = serializers.SerializerMethodField('get_hall',read_only=True)
  


    class Meta:
        model=Post
        fields=('Postid','Username','ItemName','Email' ,'Category','Description','PostDate','ImageId','Hall')
    

        


    def get_username(self,obj):
        return str(obj.Userid.username)

    def get_hall(self,obj):
        userobj = Profile.objects.get(Userid=obj.Userid)
        return userobj.Hall
    def get_email(self,obj):
       
        return obj.Userid.email 


class SearchItemSeralizer(serializers.ModelSerializer):
    Username = serializers.SerializerMethodField('get_username',read_only=True)
    Email = serializers.SerializerMethodField('get_email',read_only=True)
    Hall = serializers.SerializerMethodField('get_hall',read_only=True)


    class Meta:
        model=Post
        fields=('Postid','Username','ItemName','Email' ,'Category','Description','PostDate','ImageId','Hall')
    
        
    def get_username(self,obj):
        return str(obj.Userid.username)

    def get_hall(self,obj):
        userobj = Profile.objects.get(Userid=obj.Userid)
        return userobj.Hall
    def get_email(self,obj):
       
        return obj.Userid.email 


class get_SearchdetailSeralizer(serializers.Serializer):


    searchType = serializers.CharField(max_length=50)
    searchArg = serializers.CharField(max_length=50)
    searchOrd = serializers.CharField(max_length=50)
    class Meta:
      fields = ("searchType", "searchArg","searchOrd")

    def getSearchType(self,value):
        return value['searchType']
    
    def getSearchArg(self,value):
        return value['searchArg']
    
    def getSearchOrder(self,value):
        return value['searchOrd']


#----------------------- Make ORDER Seralizer ---------------------------------------------------------------



class  MakeOrderSeralizer(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields='__all__'

    def getUsername(self,vaildated_data):

        return vaildated_data['req_username']

    def getPostid(self,validate_data):
        return validate_data['Postid']

    def makeOrder(self,validate_data ):
        #try:
            #get the username
            userobj = User.objects.get(username=validate_data['req_username'])
            postobj = Post.objects.get(pk=validate_data['Postid'])
           
            orderobj = Order(Postid=postobj,req_Userid=userobj,Date=validate_data['Date'],Time=validate_data['Time'],Location=validate_data['Location'],
            MovingService=validate_data['MovingService'])        
            orderobj.OrderConfirm=False
            orderobj.save()
            return 1 
       # except:
        #    return 0




class get_usernameserializer(serializers.Serializer):


    username = serializers.CharField(max_length=50)

    class meta:
        fields=('username')
    
        
    def getUsername(self,vaildated_data):

        return vaildated_data['username']



#Below two seralizer is the same so technically I can just call them straight
#But I seperate them as Just in case I may need to make some changes that is unique
#to view Order await your approve and #view order make by you
class View_SenderOrderSeralizer(serializers.ModelSerializer):
    req_username = serializers.SerializerMethodField('get_username',read_only=True)
    ItemName = serializers.SerializerMethodField('get_Itemname',read_only=True)

    class Meta:
        model =Order
        fields=('OrderId', 'Postid' ,'ItemName' , 'req_username' ,'Date','Time','Location','MovingService','OrderConfirm')

    def get_username(self,orderobj):
        
        return str(orderobj.req_Userid.username)

    def get_Itemname(self,orderobj):
     
        return str(orderobj.Postid.ItemName)


class View_reqOrderSeralizer(serializers.ModelSerializer):
    from_username = serializers.SerializerMethodField('get_username',read_only=True)
    ItemName = serializers.SerializerMethodField('get_Itemname',read_only=True)

    class Meta:
        model =Order
        fields=('OrderId','Postid' , 'ItemName' , 'from_username' ,'Date','Time','Location','MovingService','OrderConfirm')

    def get_username(self,orderobj):
        
        return str(orderobj.Postid.Userid.username)

    def get_Itemname(self,orderobj):
     
        return str(orderobj.Postid.ItemName)



class Approve_Disapprove_OrderSeralizer(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields=['OrderId']
    
    def getdecision(self,validate_data):
        return validate_data['OrderConfirm']

    def getorderID(self,validate_data):
        return validate_data['OrderId']

    def implementdecision (self,validate_data ,descision):
        
        if(descision == 'False'):
            Orderobj = Order.objects.get(pk=validate_data['OrderId'])
            Orderobj.delete()
            return -1
        elif (descision == 'True'):
            Orderobj = Order.objects.get(pk=validate_data['OrderId'])
            Orderobj.OrderConfirm= True
            Orderobj.save()

            return 1



class DeleteOrderSeralizer(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields=['OrderId']
        #Need see how to picture it 
        #'__all__'
    
    def DeleteOrder(self,validated_data):
        Orderobj = Order.objects.get(pk=validated_data['OrderId'])
        Orderobj.delete()
        return 1





#---------------------------- USER ACCOUNT Seralizer ------------------------------------------------------------------------------



class LoginUserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username','password')
    
    def get_username(self ,value):
        return value['username']

    def get_password(self,value):
        return value['password']
    
    

    def checkauthentication (self ,userCode,passCode):
         user = authenticate(username= userCode, password=passCode)
            #mean the user is found
         if user is not None:
                return 1 
         else:
                return 0


class SuccessLoginSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username','email')


class CreateUserSerailizer(serializers.ModelSerializer):

    class Meta:
            model= User
            fields=('username','password','email')

    def getUsername(self,vaildated_data):
        return vaildated_data['username']
    
    def getEmail(self,vaildate_data):
        return vaildate_data['email']

    def createUser(self,validated_data):
        user =User(username=validated_data['username'] ,email=validated_data['email'])
        user.set_password(validated_data['password'])

        user.is_active =False
        
        user.save()
        profileobj = Profile(Userid=user,Hall=validated_data['Hall'])
        profileobj.save()
        return user



# EXTRA API that is not needed
# class getUsernameSeralizer(serializers.ModelSerializer):
#     class Meta:
#         model =User
#         fields=('id')   
#     def get_id(self,value):
#         return value['Userid']


#---------------------------------------- ref code ------------------------------------------------
#THIS IS SIMILAR TO FORM Model serializer mean we use the database 
#GONNA use this for Database 

#from .models import Tweet

# class TweetSerializer(serializers.ModelSerializer):
   
#     class Meta:
#         model = Tweet
#         fields=['content','id'] # we may refer to the Doc (API GUIDE) fields='_all_'
#                                 #there is also exclude 

#     #the actual value of the field
#     def validate_content(self,value):
#         if len(value) > MAX_TWEET_LENGTH:
#             raise serializers.ValidationError("You had exceed the world length of " + str(MAX_TWEET_LENGTH))

#         return value 

    

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
        fields='__all__'


    def DeletePost(self,validated_data):
        try:
            postobj = Post.objects.get(pk=validated_data['Postid'])
            postobj.delete() 
            return 1
        except:
            return 0 



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
    Order_confirm = serializers.SerializerMethodField('get_ord_con', read_only=True)


    class Meta:
        model=Post
        fields=('Postid','Username','ItemName','Email' ,'Category','Description','PostDate','ImageId','Hall','Order_confirm')
    
    
    def get_ord_con(self,obj):
        try:
            orobj = Order.objects.get(Postid= obj.Postid)
            return orobj.OrderConfirm
            #if the object does not exits
        except Order.DoesNotExist:
            return False 

        


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




class ApproveOrderSeralizer(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields='__all__'
    def approveOrder(self,validate_data):
        #get the object base on OID
        #I can do a second level check 
        #But most likely I use try and except If I can`t
        #then i delete it 
        return None 

class DeleteOrderSeralizer(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields='__all__'
        #Need see how to picture it 
        #'__all__'
    
    def DeleteOrder(self,validated_data):
        #name = Post()
        #name.save()
        return None



#---------------------------- USER ACCOUNT Seralizer ------------------------------------------------------------------------------


class getUsernameSeralizer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields=('id')   
    def get_id(self,value):
        return value['Userid']

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

    

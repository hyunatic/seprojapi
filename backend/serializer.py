
from django.conf import  settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
MAX_TWEET_LENGTH = settings.MAX_CONTENT_LENGTH


from rest_framework import serializers
#Model serializer allow us to use the existing model in model.py
# So we no need to type out all the field


#REF
#https://www.youtube.com/watch?v=TmsD8QExZ84



# just use the basic seralizer if I wish to I can use Model seralizer
# which take the auth_user model  like what is Single tweet 

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

         if user is not None:
                return 1 
         else:
                return 0


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

    

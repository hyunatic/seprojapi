from django.db import models
#taken from the website 
from django.conf import settings 
from django.contrib.auth.models import User
from datetime import datetime





# Create your models here.(Noted every changes you make to the class  we had to make migration and migrate inside the terminal)

# Assign the variable user Auth_User model which is the table that store our user..
User = settings.AUTH_USER_MODEL 


class Profile(models.Model):
    #orginally this is onetoone field but 
    Userid= models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    Hall = models.CharField(max_length=50)
    
    class Meta:
        db_table='Profile'
        managed=False

#This is your database Schema or MAP TO YOUR SQL
#Content is the column therefore 

class Post(models.Model):
    Postid = models.AutoField(primary_key=True)
    Userid = models.ForeignKey(User,on_delete=models.CASCADE ,related_name='posting')
    ItemName = models.TextField()
    Category = models.TextField()
    Description= models.TextField()
    PostDate = models.DateField()
    ImageId = models.TextField()       

    class Meta:
        db_table='Post'
        managed=False


class Order(models.Model):
    OrderId = models.AutoField(primary_key=True)
    Postid = models.ForeignKey(Post,on_delete=models.DO_NOTHING)
    req_Userid = models.ForeignKey(User,on_delete=models.DO_NOTHING )
    Date = models.DateField(default=datetime.now)
    Time = models.TimeField()
    Location = models.TextField()
    MovingService = models.BooleanField(default=False)
    OrderConfirm = models.BooleanField(default=False)

    class Meta:
        db_table='Order'
        #it will auto acreate the table field for me ... # this was set to true due to previous manual configuration for
        #order had some issues with searlizer.
        managed=True




#------------------------------------   Ref Code------------------------------------------------------------------------------------------

# class Tweet(models.Model):
#     user = models.ForeignKey(User , on_delete=models.CASCADE) # basically form a relation with the AUTH_User model
#                                                              #such as if the user is delete all the tweet belong to the user in the tweet
#     likes = models.ManyToManyField(User, related_name='tweet_user',blank=True,through=HistoryLike )                                                        # is delete 
#     content = models.TextField()
#     image = models.FileField(upload_to='images/',blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)


#     #From google a set of data the describe and give information about other data 
#     class Meta:
#         # Just a minus to sort in descending order lai dat also CAN
#         ordering =['-id']

#     #this is for our admin.py to show that this tweet content had a relation to the user
#     def __str__(self):
#         return self.content
    


    # FOR PURE JAVASCRIPT you need this method
    # def serialize(self):
    #     #return the JSON format  or seralize it to look like JSON format
    #     return {

    #         "id": self.id,
    #         "content": self.content,
    #          #"user": self.user
    #     }

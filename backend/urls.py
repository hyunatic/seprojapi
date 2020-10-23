"""SE_master URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from backend import views
from backend import Verifyaccount 

urlpatterns = [

    path('admin/', admin.site.urls),



    #Link to function view there is also Class API view 
    #For User credential
    path('activate/<uidb64>/<token>',Verifyaccount.VertificationView.as_view(),name="activate"),
    path('api/create_User', views.create_User),
    path('api/check_Login',views.login),
    path('api/get_Username',views.get_username),

    #For Post
    path('api/view_Item',views.list_view),
    path('api/view_User_Item',views.list_user_view),
    path('api/search_Item',views.search_post_Item),
    path('api/post_Item',views.postItem),
    path('api/delete_Item',views.DeleteItem),
     
    #For Order
    path('api/make_Order',views.makeOrder),

   
]


#--------------------------------- REF CODE----------------------------------------------------------------------   # path('',views.home_view),
    #path('create', views.create_tweet_view),
    # path('api/listview', views.list_view),
    #path('api/search_Item/<str:Username>',views.list_single_view),
    

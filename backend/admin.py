from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as baseAdmin
from django.contrib.auth.models import User
from .models import Post,Order,Profile


#register the two table that I had created 
admin.site.register(Post)
admin.site.register(Order)


class proflieinLine(admin.StackedInline):
    model = Profile
    can_delete= False
    verbose_name_plural="Profile"


class UserAdmin(baseAdmin):
    inlines=(proflieinLine,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
    #----------------------- Ref code to customize Django Admin --------------------------------
#from .models import Tweet, HistoryLike
# Register your models here.
#to show our Tweet table (NOTE OUR SQL NEED TO HAVE IT)


# class HistoryLikeAdmin(admin.TabularInline):
#    model = HistoryLike


# class TestAdmin(admin.ModelAdmin):
#     inlines = [HistoryLikeAdmin]
#     list_display =['__str__','user'] #you can add the  __str__ method in your model class to display something
#     search_fields=['content','user__username']

#     class meta :
#         model = Tweet 

# admin.site.register(Tweet,TestAdmin)

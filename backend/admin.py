from django.contrib import admin






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
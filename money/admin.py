from django.contrib import admin
from .models import *
# Register your models here.


class User_List(admin.ModelAdmin):
    list_display=('Username','Email','Password','Balance')
admin.site.register(User,User_List)


admin.site.register(Transection_Category)

admin.site.register(Transection_Type)

class Transection_History_list(admin.ModelAdmin):
    list_display=('uid','Date','Description','transection_Type','Category','Amount',)
admin.site.register(Transection_History,Transection_History_list)
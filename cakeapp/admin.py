from django.contrib import admin
from cakeapp.models import Cake
# Register your models here.

class CakeAdmin(admin.ModelAdmin):
    list_display=['id','name','cat','cdetail','price']

admin.site.register(Cake,CakeAdmin)
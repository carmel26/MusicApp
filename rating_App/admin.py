from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(Rating)  
admin.site.register(Music) 
admin.site.register(CustomUserTable) 
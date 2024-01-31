from django.contrib import admin
#from django.contrib.admin.decorators import ad
# Register your models here.
from .models import User

admin.site.register(User)

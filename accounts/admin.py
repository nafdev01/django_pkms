# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *
from django.conf import settings

admin.site.register(Profile)
admin.site.register(Student)

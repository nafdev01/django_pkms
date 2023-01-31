# notes/admins.py
from django.contrib import admin
from notes.models import *

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Entry)
# revision.admin.py
from django.contrib import admin
from revision.models import *

admin.site.register(Objective)

@admin.register(SubObjective)
class SubObjectiveAdmin(admin.ModelAdmin):
    list_display = ["number","name", "complete"]
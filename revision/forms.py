# notes/forms.py
from django.utils.translation import gettext_lazy as _
from django import forms
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from notes.models import *
from revision.models import *


class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['name', 'start_date', 'end_date', 'description']
        widgets = {
            "start_date": DatePickerInput(),
            "end_date": DatePickerInput(),
        }

     

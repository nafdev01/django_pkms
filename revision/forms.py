# notes/forms.py
from django.utils.translation import gettext_lazy as _
from django import forms
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from notes.models import *
from revision.models import *


class ObjectiveForm(forms.ModelForm):
    def __init__(self, student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(student=student)

    class Meta:
        model = Objective
        fields = ["name", "course", "start_date", "end_date", "description", "complete"]
        widgets = {
            "start_date": DatePickerInput(),
            "end_date": DatePickerInput(),
        }

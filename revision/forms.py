# notes/forms.py
from django.utils.translation import gettext_lazy as _
from django import forms
from .widgets import DatePickerInput
from notes.models import *
from revision.models import *
from markdownx.widgets import MarkdownxWidget


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
            "description": MarkdownxWidget(attrs={"rows": 10}),
        }


class SubObjectiveForm(forms.ModelForm):
    def __init__(self, student, course, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["topic"].queryset = Topic.objects.filter(
            course_id=course.id, course__student=student
        )

    class Meta:
        model = SubObjective
        fields = [
            "number",
            "name",
            "topic",
            "start_date",
            "end_date",
            "complete",
        ]
        widgets = {
            "start_date": DatePickerInput(),
            "end_date": DatePickerInput(),
        }

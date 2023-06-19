# notes/forms.py
from django.utils.translation import gettext_lazy as _
from django import forms
from notes.models import *
from markdownx.widgets import MarkdownxWidget

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "course_code", "course_type", "about"]


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["number", "name", "overview"]


class SubTopicForm(forms.ModelForm):
    class Meta:
        model = SubTopic
        fields = ["number", "name"]


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["name", "content", "revised"]
        widgets = {"content": MarkdownxWidget(attrs={"cols": 80, "rows": 20})}

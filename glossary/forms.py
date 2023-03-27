# glossary/forms.py
from django.utils.translation import gettext_lazy as _
from django import forms
from glossary.models import *


class TermForm(forms.ModelForm):
    def __init__(self, student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(student=student)

    class Meta:
        model = Term
        fields = ["course", "name", "definition"]


class TermInlineForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ["name", "definition"]

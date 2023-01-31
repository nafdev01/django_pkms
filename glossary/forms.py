# glossary/forms.py
from django.utils.translation import gettext_lazy as _
from django import forms
from glossary.models import *


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ["course","name","definition"]

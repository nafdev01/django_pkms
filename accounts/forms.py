# accounts/forms.py
from django.utils.translation import gettext_lazy as _
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.conf import settings
from .models import *


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ("username",)
        field_classes = {"username": UsernameField}


# form for editing a user object
class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["username", "first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = Student.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use.")
        return data


# form for editing a user object
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["degree", "date_of_birth", "year", "photo"]
        widgets = {
            "date_of_birth": DatePickerInput(),
        }


# class DeleteAccountForm(forms.ModelForm):
#     confirm_delete = forms.BooleanField(label="Confirm deletion", required=True)

#     class Meta:
#         model = Student
#         fields = []

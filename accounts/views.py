from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from accounts.models import *
from notes.models import *
from .forms import *


class UserLoginView(LoginView):
    redirect_authenticated_user = True


def register(request):
    if request.method != "POST":
        student_form = StudentRegistrationForm()
    else:
        student_form = StudentRegistrationForm(request.POST)
        if student_form.is_valid():
            # create a new user object without saving it
            new_student = student_form.save(commit=False)
            # set chosen password
            new_student.set_password(student_form.cleaned_data["password1"])
            # save the user object
            student_form.save()
            # create a new profile object for the user object
            Profile.objects.create(student=new_student)

            messages.success(request, "Registration Successful! Log in to continue")
            return redirect("login")

    template_path = "registration/signup.html"
    context = {"form": student_form}
    return render(request, template_path, context)

@login_required
def profile(request, user_id=None, username=None):
    student=request.user

    Profile.objects.get_or_create(student=student)

    profile = student.profile
    certifications = Course.certifications.filter(student_id=student.id)
    coursework = Course.coursework_modules.filter(student_id=student.id)

    template_path = "accounts/profile.html"
    context = {
        "student": student,
        "profile": profile,
        "section": "profile",
        "certifications": certifications,
        "coursework": coursework,
    }
    return render(request, template_path, context)


@login_required
def edit_profile(request):
    student = request.user
    profile = student.profile
    if request.method != "POST":
        student_update_form = StudentUpdateForm(instance=student)
        profile_edit_form = ProfileEditForm(instance=profile)
    else:
        student_update_form = StudentUpdateForm(
            instance=student,
            data=request.POST,
        )
        profile_edit_form = ProfileEditForm(
            instance=profile,
            data=request.POST,
            files=request.FILES,
        )
        if student_update_form.is_valid() and profile_edit_form.is_valid():
            student_update_form.save()
            profile_edit_form.save()
            messages.success(request, "Profile Updated successfully")
            return redirect(student.profile)
        else:
            messages.error(request, "Error Updating Your Profile")

    template_path = "accounts/edit_profile.html"
    context = {
        "student_update_form": student_update_form,
        "profile_edit_form": profile_edit_form,
        "section": "profile",
    }
    return render(request, template_path, context)

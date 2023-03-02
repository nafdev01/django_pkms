from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_student
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.models import *
from notes.models import *
from accounts.forms import *


def login(request):
    if request.user.is_authenticated:
        # redirect to home page if user is already logged in
        messages.warning(request, "You are already logged in.")
        return redirect("notes:dashboard")
    else:
        if request.method != "POST":
            form = AuthenticationForm()
        else:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                student = authenticate(
                    request,
                    username=username,
                    password=password,
                )

                if student is not None:
                    login_student(request, student)
                    # redirect to profile page on successful login
                    messages.success(request, f"Welcome, {student.get_username()}")
                    return redirect("profile")
                else:
                    # show error message if login fails
                    messages.warning(
                        request, "Incorrect login credentials... please try again."
                    )

    template_path = "registration/login.html"
    context = {"form": form}
    return render(request, template_path, context)


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
    student = request.user

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

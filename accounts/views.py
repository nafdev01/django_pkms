import os
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_student
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.models import *
from notes.models import *
from accounts.forms import *
from accounts.two_factor_auth import *


def login(request):
    if request.user.is_authenticated:
        # redirect to home page if user is already logged in
        messages.warning(request, "You are already logged in.")
        return redirect("notes:dashboard")

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
                # check if 2FA is enabled for the student
                try:
                    two_factor = TwoFactorAuth.objects.get(student=student)
                    generate_2fa(student)
                except TwoFactorAuth.DoesNotExist:
                    generate_2fa(student)

                request.session["student_id"] = student.id
                return redirect("display_qrcode")

    template_path = "registration/login.html"
    context = {"form": form}
    return render(request, template_path, context)


def display_qrcode(request):
    student_id = request.session["student_id"]
    student = get_object_or_404(Student, id=student_id)

    # Render the QR code image using a template
    template_path = "accounts/2fa/display_qrcode.html"
    context = {
        "student": student,
        "qrcode_url": os.path.join(
            settings.MEDIA_URL, f"user_{student.get_username()}", "2fa", "qr_code.png"
        ),
    }
    return render(request, template_path, context)


def verify_2fa(request):
    student_id = request.session["student_id"]
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get("otp")

            # Verify the OTP
            if authenticate_2fa(student, otp):
                # OTP is valid, login the user
                login_student(request, student)
                messages.success(request, "Welcome back!")
                return redirect("profile")
            else:
                # OTP is invalid
                messages.error(request, "Invalid OTP. Please try again.")
    else:
        form = TwoFactorForm()

    return render(request, "accounts/2fa/verify_2fa.html", {"form": form})


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

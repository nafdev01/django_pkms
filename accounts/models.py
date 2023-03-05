# accounts/models.py
import os
import pyotp
import qrcode
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from datetime import date


def generate_2fa(instance):
    student = instance.student
    two_factor, created = TwoFactorAuth.objects.get_or_create(student=student)
    secret = two_factor.secret

    # Print the QR code URL
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=student.twofactorauth.name,
        issuer_name=student.twofactorauth.issuer,
    )
    img = qrcode.make(uri)

    # Define the file path
    file_path = f"user_{instance.student.get_username()}/2fa/qr_code.png"

    # Save the QR code as an image
    img.save(file_path)

    # set the two_factor_status to enabled
    two_factor.two_factor_status = TwoFactorAuth.TwoFactorStatus.ENABLED
    two_factor.save()
    return


def student_profile_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.student.username}/profile_photo/{filename}"


def student_2fa_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.student.username}/profile_photo/{filename}"


# student model
class Student(AbstractUser):
    """
    Description: Custom Student Model
    """

    def age(self):
        today = date.today()
        age = (
            today.year
            - self.profile.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.profile.date_of_birth.month, self.profile.date_of_birth.day)
            )
        )
        return age


class Profile(models.Model):
    """
    Description: Student Profile Model
    """

    # choices for student year
    class StudentYear(models.TextChoices):
        FIRST = "1", "First Year"
        SECOND = "2", "Second Year"
        THIRD = "3", "Third Year"
        FOURTH = "4", "Fourth Year"
        FIFTH = "5", "Fifth Year"
        SIXTH = "6", "Sixth Year"

    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    degree = models.CharField(
        max_length=250, default="Not applicable", blank=True, null=True
    )

    date_of_birth = models.DateField(blank=True, null=True)

    year = models.CharField(
        max_length=2, choices=StudentYear.choices, default=StudentYear.FIRST
    )
    photo = models.ImageField(
        upload_to=student_profile_photo_path, blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse(
            f"profile",
        )

    def __str__(self):
        return f"{self.student}'s profile"

    class Meta:
        ordering = ["student"]


#  student model
class TwoFactorAuth(models.Model):
    """
    Description: Custom Student Model
    """

    # choices for 2fa authentication status
    class Status2FA(models.TextChoices):
        DISABLED = "DA", "Not Enabled"
        ENABLED = "EN", "Enabled not Activated"
        ACTIVATED = "AC", "Enabled and Activated"

    student = models.OneToOneField(Student, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=2,
        choices=Status2FA.choices,
        default=Status2FA.DISABLED,
        editable=False,
    )

    name = models.CharField(max_length=250, editable=False)
    issuer = models.CharField(max_length=250, editable=False, default="Django PKMS")
    secret = models.CharField(max_length=250, null=True, editable=False)
    qrcode = models.ImageField(upload_to=student_2fa_photo_path, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.student.username
        if not self.secret:
            self.secret = pyotp.random_base32()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student}'s 2fa"

    class Meta:
        ordering = ["student"]

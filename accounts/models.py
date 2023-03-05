# accounts/models.py
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from datetime import date


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

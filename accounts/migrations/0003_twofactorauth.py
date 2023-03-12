# Generated by Django 4.1.7 on 2023-03-05 09:36

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_delete_twofactorauth"),
    ]

    operations = [
        migrations.CreateModel(
            name="TwoFactorAuth",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DA", "Not Enabled"),
                            ("EN", "Enabled not Activated"),
                            ("AC", "Enabled and Activated"),
                        ],
                        default="DA",
                        editable=False,
                        max_length=2,
                    ),
                ),
                ("name", models.CharField(editable=False, max_length=250)),
                (
                    "issuer",
                    models.CharField(
                        default="Django PKMS", editable=False, max_length=250
                    ),
                ),
                ("secret", models.CharField(editable=False, max_length=250, null=True)),
                (
                    "qrcode",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=accounts.models.student_2fa_photo_path,
                    ),
                ),
                (
                    "student",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["student"],
            },
        ),
    ]
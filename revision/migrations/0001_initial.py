# Generated by Django 4.1.7 on 2024-03-31 08:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("notes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Objective",
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
                ("name", models.CharField(max_length=250)),
                (
                    "slug",
                    models.SlugField(
                        blank=True, editable=False, max_length=250, null=True
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("number", models.IntegerField(default=0)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("description", models.TextField(blank=True)),
                ("duration", models.IntegerField(editable=False)),
                ("complete", models.BooleanField(default=False)),
                (
                    "course",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notes.course",
                    ),
                ),
            ],
            options={
                "verbose_name": "objective",
                "verbose_name_plural": "objectives",
                "ordering": ["start_date", "end_date", "complete", "course"],
                "unique_together": {("name", "course")},
            },
        ),
        migrations.CreateModel(
            name="SubObjective",
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
                ("name", models.CharField(max_length=250)),
                (
                    "slug",
                    models.SlugField(
                        blank=True, editable=False, max_length=250, null=True
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("number", models.IntegerField(default=0)),
                ("duration", models.IntegerField(editable=False)),
                ("complete", models.BooleanField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "objective",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="revision.objective",
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notes.topic",
                    ),
                ),
            ],
            options={
                "verbose_name": "sub objective",
                "verbose_name_plural": "sub objectives",
                "ordering": ["-complete", "number", "start_date", "end_date", "topic"],
                "unique_together": {("name", "topic")},
            },
        ),
    ]

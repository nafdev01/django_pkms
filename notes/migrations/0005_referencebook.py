# Generated by Django 4.2.2 on 2023-06-18 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("notes", "0004_alter_course_course_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReferenceBook",
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
                ("title", models.CharField()),
                (
                    "slug",
                    models.SlugField(
                        blank=True, editable=False, max_length=250, null=True
                    ),
                ),
                ("author", models.CharField()),
                ("date_of_publication", models.DateTimeField()),
                ("edition", models.CharField()),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notes.course",
                    ),
                ),
            ],
            options={
                "verbose_name": "entry",
                "verbose_name_plural": "entries",
                "ordering": ["course", "title"],
                "unique_together": {("title", "course")},
            },
        ),
    ]

# Generated by Django 4.2.2 on 2023-06-18 12:01

from django.db import migrations, models
import notes.models


class Migration(migrations.Migration):
    dependencies = [
        ("notes", "0009_referencebook_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="referencebook",
            name="file",
            field=models.FileField(
                blank=True, null=True, upload_to=notes.models.reference_book_path
            ),
        ),
    ]

# Generated by Django 4.2.2 on 2023-06-24 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("notes", "0001_initial"),
        ("revision", "0003_subobjective_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subobjective",
            name="topic",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="notes.topic"
            ),
        ),
    ]

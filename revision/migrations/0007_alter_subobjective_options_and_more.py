# Generated by Django 4.2.2 on 2023-06-25 07:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("revision", "0006_alter_subobjective_complete"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subobjective",
            options={
                "ordering": ["number", "start_date", "end_date", "complete", "topic"],
                "verbose_name": "sub objective",
                "verbose_name_plural": "sub objectives",
            },
        ),
        migrations.RemoveField(
            model_name="subobjective",
            name="description",
        ),
    ]

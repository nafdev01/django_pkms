# Generated by Django 4.1.7 on 2023-03-02 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_student_two_factor_secret_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='twofactorauth',
            name='two_factor_secret',
            field=models.CharField(max_length=250, null=True),
        ),
    ]

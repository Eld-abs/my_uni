# Generated by Django 5.1.2 on 2024-11-15 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_lesson_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='details',
        ),
        migrations.AddField(
            model_name='groupstudents',
            name='details',
            field=models.JSONField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-15 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_groupstudents_photo_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='description',
            field=models.CharField(max_length=250, null=True),
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-09 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactinfo',
            name='alternative_phone_number',
        ),
    ]

# Generated by Django 5.1.5 on 2025-02-01 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_rename_contact_mess_contact_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messmenu',
            name='snacks',
        ),
        migrations.AddField(
            model_name='messmenu',
            name='snacks_available',
            field=models.BooleanField(default=False),
        ),
    ]

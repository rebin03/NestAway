# Generated by Django 5.1.5 on 2025-01-30 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_alter_property_bathroom_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='mess_included',
            field=models.BooleanField(default=True),
        ),
    ]

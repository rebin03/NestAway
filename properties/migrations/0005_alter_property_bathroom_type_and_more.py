# Generated by Django 5.1.5 on 2025-01-30 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_delete_propertylocation_property_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='bathroom_type',
            field=models.CharField(blank=True, choices=[('COMMON', 'Common'), ('SINGLE', 'Single'), ('ATTACHED', 'Attached')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='mess_included',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

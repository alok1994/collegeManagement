# Generated by Django 4.2.5 on 2023-11-04 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissionapp', '0007_admissionform_current_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionform',
            name='dist',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='admissionform',
            name='pin_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='admissionform',
            name='state',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
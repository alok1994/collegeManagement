# Generated by Django 4.2.5 on 2023-10-18 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissionapp', '0004_alter_admissionform_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionform',
            name='registration_number',
            field=models.CharField(default=2, max_length=20),
            preserve_default=False,
        ),
    ]
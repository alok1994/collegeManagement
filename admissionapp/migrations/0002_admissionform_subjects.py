# Generated by Django 4.2.5 on 2023-10-12 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissionapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionform',
            name='subjects',
            field=models.CharField(default=2, max_length=1000),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.5 on 2023-10-26 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee_management', '0003_fee_discount_fee_fee_late_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='remaining_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
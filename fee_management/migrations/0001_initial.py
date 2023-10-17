# Generated by Django 4.2.5 on 2023-10-15 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admissionapp', '0004_alter_admissionform_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tuition_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('exam_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sports_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('miscellaneous_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_date', models.DateField()),
                ('fee_for_month', models.CharField(max_length=255)),
                ('receipt_number', models.CharField(max_length=20)),
                ('total_paid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_amount_in_words', models.CharField(max_length=10000)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admissionapp.admissionform')),
            ],
        ),
    ]

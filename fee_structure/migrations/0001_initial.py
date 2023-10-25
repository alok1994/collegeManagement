# Generated by Django 4.2.5 on 2023-10-24 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.PositiveIntegerField(unique=True)),
                ('tuition_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('exam_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sport_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('miscellaneous_fee', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
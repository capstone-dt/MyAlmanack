# Generated by Django 2.1.5 on 2019-03-12 20:33

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myalmanack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birthday',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2019, 3, 12))]),
        ),
    ]
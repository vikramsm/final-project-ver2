# Generated by Django 2.0.3 on 2019-05-16 19:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dicomapp', '0005_auto_20190516_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='date',
            field=models.DateField(default=datetime.date(2019, 5, 17)),
        ),
        migrations.AlterField(
            model_name='admission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2019, 5, 16, 19, 29, 18, 362263, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(default=datetime.date(2019, 5, 17)),
        ),
        migrations.AlterField(
            model_name='medicaltest',
            name='date',
            field=models.DateField(default=datetime.date(2019, 5, 17)),
        ),
        migrations.AlterField(
            model_name='patientfiles',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 16, 19, 29, 18, 371264, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateField(default=datetime.date(2019, 5, 17)),
        ),
    ]

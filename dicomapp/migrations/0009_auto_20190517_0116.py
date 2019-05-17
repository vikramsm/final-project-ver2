# Generated by Django 2.0.3 on 2019-05-16 19:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dicomapp', '0008_auto_20190517_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='time',
            field=models.TimeField(default=datetime.datetime(2019, 5, 16, 19, 46, 49, 544079, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='birthday',
            field=models.DateField(default=datetime.date(1900, 1, 1)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='birthday',
            field=models.DateField(default=datetime.date(1900, 1, 1)),
        ),
        migrations.AlterField(
            model_name='patientfiles',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 16, 19, 46, 49, 553082, tzinfo=utc)),
        ),
    ]

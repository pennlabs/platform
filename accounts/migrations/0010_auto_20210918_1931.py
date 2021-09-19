# Generated by Django 3.1.7 on 2021-09-18 23:31

import datetime

import django.utils.timezone
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_auto_20210918_1744"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="verification_timestamp",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(2021, 9, 18, 23, 31, 40, 44197, tzinfo=utc),
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="phonenumber",
            name="verification_timestamp",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
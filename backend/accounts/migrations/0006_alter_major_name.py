# Generated by Django 4.2.6 on 2023-10-14 04:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_privacyresource_privacysetting"),
    ]

    operations = [
        migrations.AlterField(
            model_name="major",
            name="name",
            field=models.CharField(max_length=150),
        ),
    ]

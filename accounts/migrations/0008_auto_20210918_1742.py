# Generated by Django 3.1.7 on 2021-09-18 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_auto_20210402_1257"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="value",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]

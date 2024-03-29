# Generated by Django 4.1.3 on 2022-11-10 02:05

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_auto_20210918_2041"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="profile_pic",
            field=models.ImageField(
                blank=True, null=True, upload_to=accounts.models.get_user_image_filepath
            ),
        ),
    ]

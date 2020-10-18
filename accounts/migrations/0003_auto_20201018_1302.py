# Generated by Django 3.1.2 on 2020-10-18 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_auto_20200213_1711"),
    ]

    operations = [
        migrations.AddField(
            model_name="student", name="graduation_year", field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="preferred_name",
            field=models.CharField(blank=True, max_length=225),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="first name"),
        ),
        migrations.CreateModel(
            name="PhoneNumberModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, default=None, max_length=128, region=None, unique=True
                    ),
                ),
                ("primary", models.BooleanField(default=False)),
                ("verification_code", models.CharField(blank=True, max_length=6, null=True)),
                ("verification_timestamp", models.DateTimeField(blank=True, null=True)),
                ("verified", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="phone_numbers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Email",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("primary", models.BooleanField(default=False)),
                ("verification_code", models.CharField(blank=True, max_length=6, null=True)),
                ("verification_timestamp", models.DateTimeField(blank=True, null=True)),
                ("verified", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emails",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

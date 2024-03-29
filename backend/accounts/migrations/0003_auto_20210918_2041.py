# Generated by Django 3.2.7 on 2021-09-19 00:41

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


def create_student_objects(apps, schema_editor):
    """
    Create student objects for each user account by forcing a user account
    save for each user.
    """

    User = apps.get_model("accounts", "User")
    for u in User.objects.all():
        u.save()


def create_email_objects(apps, schema_editor):
    """
    Create a new primary, verified email for each user based on their email
    found from the directory
    """
    User = apps.get_model("accounts", "User")
    Email = apps.get_model("accounts", "Email")
    for u in User.objects.all():
        Email.objects.create(user=u, value=u.email, primary=True, verified=True)
        u.email = ""
        u.save()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_auto_20200213_1711"),
    ]

    operations = [
        migrations.CreateModel(
            name="Major",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "degree_type",
                    models.CharField(
                        choices=[
                            ("BACHELORS", "Bachelor's"),
                            ("MASTERS", "Master's"),
                            ("PHD", "PhD"),
                            ("PROFESSIONAL", "Professional"),
                        ],
                        default="PROFESSIONAL",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="student",
            name="graduation_year",
            field=models.PositiveIntegerField(
                null=True, validators=[django.core.validators.MinValueValidator(1740)]
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="preferred_name",
            field=models.CharField(blank=True, max_length=225),
        ),
        migrations.RemoveField(
            model_name="student",
            name="major",
        ),
        migrations.RemoveField(
            model_name="student",
            name="school",
        ),
        migrations.AlterField(
            model_name="student",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="student",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
        migrations.CreateModel(
            name="PhoneNumber",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "value",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        default=None,
                        max_length=128,
                        region=None,
                        unique=True,
                    ),
                ),
                ("primary", models.BooleanField(default=False)),
                (
                    "verification_code",
                    models.CharField(blank=True, max_length=6, null=True),
                ),
                ("verification_timestamp", models.DateTimeField(auto_now_add=True)),
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
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.EmailField(max_length=254, unique=True)),
                ("primary", models.BooleanField(default=False)),
                (
                    "verification_code",
                    models.CharField(blank=True, max_length=6, null=True),
                ),
                ("verification_timestamp", models.DateTimeField(auto_now_add=True)),
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
        migrations.AddField(
            model_name="student",
            name="major",
            field=models.ManyToManyField(blank=True, to="accounts.Major"),
        ),
        migrations.AddField(
            model_name="student",
            name="school",
            field=models.ManyToManyField(blank=True, to="accounts.School"),
        ),
        migrations.RunPython(create_student_objects),
        migrations.RunPython(create_email_objects),
    ]

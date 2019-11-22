# Generated by Django 2.2 on 2019-04-07 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("accounts", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("order", models.IntegerField(null=True, unique=True)),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("tagline", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("order", models.IntegerField(null=True, unique=True)),
                ("url", models.URLField()),
            ],
            options={"ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("bio", models.TextField()),
                ("job", models.CharField(blank=True, max_length=255, null=True)),
                ("location", models.CharField(max_length=255)),
                ("url", models.SlugField(unique=True)),
                ("photo", models.URLField()),
                ("linkedin", models.URLField(blank=True, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("github", models.URLField(blank=True, null=True)),
                ("graduation_year", models.IntegerField(blank=True, null=True)),
                ("year_joined", models.DateField()),
                ("alumnus", models.BooleanField(default=False)),
                ("roles", models.ManyToManyField(to="org.Role")),
                (
                    "student",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="accounts.Student",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="members",
                        to="org.Team",
                    ),
                ),
            ],
            options={"ordering": ["student__user__first_name"]},
        ),
    ]

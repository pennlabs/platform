# Generated by Django 2.1.2 on 2018-12-10 22:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('org', '0002_auto_20181210_2213'),
        ('engagement', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Student',
        ),
    ]

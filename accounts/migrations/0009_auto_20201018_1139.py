# Generated by Django 3.1.2 on 2020-10-18 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200913_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='major',
        ),
        migrations.AddField(
            model_name='student',
            name='major',
            field=models.ManyToManyField(to='accounts.Major'),
        ),
    ]

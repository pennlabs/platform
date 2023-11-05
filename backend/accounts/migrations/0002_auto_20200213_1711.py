# Generated by Django 3.0.3 on 2020-02-13 22:11

from django.db import migrations, transaction


def create_groups(apps, schema_editor):
    with transaction.atomic():
        User = apps.get_model("accounts", "User")
        Group = apps.get_model("auth", "Group")
        for user in User.objects.all():
            for affiliation in user.affiliation.all():
                if affiliation.name is not None:
                    group, _ = Group.objects.get_or_create(name=affiliation.name)
                    user.groups.add(group)
            user.save()


def copy_permissions(apps, schema_editor):
    with transaction.atomic():
        User = apps.get_model("accounts", "User")
        Permission = apps.get_model("auth", "Permission")
        ContentType = apps.get_model("contenttypes", "ContentType")
        for user in User.objects.all():
            for product_permission in user.product_permission.all():
                content_type = ContentType.objects.get(
                    app_label="accounts", model="user"
                )
                perm, _ = Permission.objects.get_or_create(
                    codename=product_permission.id,
                    name=product_permission.name,
                    content_type=content_type,
                )
                user.user_permissions.add(perm)
            user.save()


class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial")]

    operations = [
        migrations.RunPython(create_groups),
        migrations.RemoveField(model_name="user", name="affiliation"),
        migrations.DeleteModel(name="PennAffiliation"),
        migrations.RunPython(copy_permissions),
        migrations.RemoveField(model_name="user", name="product_permission"),
        migrations.DeleteModel(name="ProductPermission"),
    ]

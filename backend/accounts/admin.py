from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Email, Major, PhoneNumber, School, Student, User


class EmailAdmin(admin.ModelAdmin):
    search_fields = ("email")
    readonly_fields = ("email")


class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    list_display = ("username", "first_name", "last_name")
    list_filter = ("school", "major")

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("username", "pennid", "last_login", "date_joined")
    search_fields = ("username", "first_name", "last_name")
    list_display = ("username", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    filter_horizontal = ("groups", "user_permissions")
    ordering = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "pennid")}),
        (
            ("Personal info"),
            {"fields": ("first_name", "preferred_name", "last_name", "email")},
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


class MajorAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_filter = ("is_active", "degree_type")
    list_display = ("name",)


class SchoolAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = ("name",)


admin.site.register(Permission)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(PhoneNumber)
admin.site.register(Email, EmailAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(School, SchoolAdmin)


class LabsAdminSite(admin.AdminSite):
    """
    Custom admin site that redirects users to log in through shibboleth
    instead of logging in with a username and password
    """

    def login(self, request, extra_context=None):
        if not request.user.is_authenticated:
            return redirect(
                reverse("accounts:login") + "?next=" + request.GET.get("next")
            )
        return super().login(request, extra_context)


if settings.SHIB_ADMIN:
    """
    Replace the default admin site with a custom one to log in users through shibboleth.
    Also copy all registered models from the default admin site
    """
    labs_admin = LabsAdminSite()
    labs_admin._registry = admin.site._registry
    admin.site = labs_admin

from django.contrib import admin
from django.contrib.auth.models import Permission

from accounts.models import Student, User


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
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            ("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(Permission)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)

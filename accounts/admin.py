from django.contrib import admin

from accounts.models import PennAffiliation, ProductPermission, Student, User


class StudentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
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
    list_filter = ("is_staff", "is_superuser", "is_active", "affiliation")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "pennid",
                    "first_name",
                    "last_name",
                    "email",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "affiliation",
                    "product_permission",
                    "last_login",
                    "date_joined",
                )
            },
        ),
        ("Advanced", {"classes": ("collapse",), "fields": ("groups", "user_permissions")}),
    )


admin.site.register(PennAffiliation)
admin.site.register(ProductPermission)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)

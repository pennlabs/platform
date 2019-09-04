from django.contrib import admin

from accounts.models import PennAffiliation, ProductPermission, Student, User


class StudentAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_display = ('username', 'first_name', 'last_name')
    list_filter = ('school', 'major')

    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)
    search_fields = ('username', 'first_name', 'last_name')
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


admin.site.register(PennAffiliation)
admin.site.register(ProductPermission)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)

from django.contrib import admin

from accounts.models import PennAffiliation, ProductPermission, Student, User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)
    search_fields = ('username', 'first_name', 'last_name')
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


admin.site.register(PennAffiliation)
admin.site.register(ProductPermission)
admin.site.register(Student)
admin.site.register(User, UserAdmin)

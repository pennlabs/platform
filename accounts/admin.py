from django.contrib import admin

from accounts.models import PennAffiliation, ProductPermission, Student, User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)


admin.site.register(PennAffiliation)
admin.site.register(ProductPermission)
admin.site.register(Student)
admin.site.register(User, UserAdmin)

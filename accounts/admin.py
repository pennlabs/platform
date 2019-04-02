from django.contrib import admin

from accounts.models import Student


class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)


admin.site.register(Student, StudentAdmin)

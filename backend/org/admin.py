from django.contrib import admin

from org.models import Member, Role, Team


class MemberAdmin(admin.ModelAdmin):
    autocomplete_fields = ["student"]


admin.site.register(Member, MemberAdmin)
admin.site.register(Role)
admin.site.register(Team)

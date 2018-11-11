from django.contrib import admin
from clubs.models import Club, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'club', 'time')
    list_filter = ()
    raw_id_fields = ()


admin.site.register(Club)
admin.site.register(Event, EventAdmin)

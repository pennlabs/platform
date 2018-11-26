from django.contrib import admin
from clubs.models import Club, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'club', 'start_time')


admin.site.register(Club)
admin.site.register(Event, EventAdmin)

from django.contrib import admin
from .models import LabMember, Team, Update, Event
from accounts.models import User

admin.site.register(User)
admin.site.register(LabMember)
admin.site.register(Team)
admin.site.register(Update)
admin.site.register(Event)

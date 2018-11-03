from django.contrib import admin
from .models import Member, Team, Role, Update, Event
from accounts.models import User

admin.site.site_header = "Platform API Admin"
admin.site.register(User)
admin.site.register(Member)
admin.site.register(Team)
admin.site.register(Role)
admin.site.register(Update)
admin.site.register(Event)

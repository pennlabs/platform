from django.contrib import admin
from org.models import Member, Team, Role
from accounts.models import User


admin.site.register(User)
admin.site.register(Member)
admin.site.register(Team)
admin.site.register(Role)

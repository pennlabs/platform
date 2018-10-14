from django.contrib import admin
from .models import LabMember, Product, Update, Event
from accounts.models import User

admin.site.register(User)
admin.site.register(LabMember)
admin.site.register(Product)
admin.site.register(Update)
admin.site.register(Event)

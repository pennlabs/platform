from django.contrib import admin
from .models import Member, Product, Update, Event

admin.site.register(Member)
admin.site.register(Product)
admin.site.register(Update)
admin.site.register(Event)
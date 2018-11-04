from django.contrib import admin
from services.models import Service, Endpoint, Update


admin.site.register(Service)
admin.site.register(Endpoint)
admin.site.register(Update)
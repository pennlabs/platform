from django.contrib import admin

from services.models import Endpoint, Service, Update


admin.site.register(Endpoint)
admin.site.register(Service)
admin.site.register(Update)

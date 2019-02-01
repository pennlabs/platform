from django.contrib import admin, messages
from accounts.models import Student, Application
from accounts.utils import assign_client_secret


class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin for Application model
    Logic from: https://github.com/florimondmanca/djangorestframework-api-key
    """
    def get_readonly_fields(self, request, obj=None):
        return ('client_id', 'hashed_secret')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            secret_key = assign_client_secret(obj)
            obj.save()
            message = "Your secret key is {}".format(secret_key)
            messages.add_message(request, messages.WARNING, message)
        else:
            obj.save()


admin.site.register(Student)
admin.site.register(Application, ApplicationAdmin)

from django.http import HttpResponseForbidden
from oauth2_provider.views import ProtectedResourceView
from oauth2_provider.views.mixins import ProtectedResourceMixin


class LabsMixin(ProtectedResourceMixin):
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "student") and hasattr(request.user.student, "member"):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()


class PennView(ProtectedResourceView):
    pass


class LabsView(LabsMixin, ProtectedResourceView):
    pass

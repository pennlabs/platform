from django.urls import path
from penngroups.views import PennGroupsGetGroupsView


app_name = "penngroups"

urlpatterns = [
    path("groups/", PennGroupsGetGroupsView.as_view(), name="agh"),
]

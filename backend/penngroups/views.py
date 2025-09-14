import requests
from http import HTTPStatus
from django.http import JsonResponse
from django.views.generic import View

from Platform.settings.base import PENN_GROUPS_PWD, PENN_GROUPS_USER


class PennGroupsGetGroupsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=HTTPStatus.UNAUTHORIZED)
        if request.user.pennid is None:
            return JsonResponse({"message": "Unknown user"}, status=HTTPStatus.NOT_FOUND)
        
        url = f"https://grouperWs.apps.upenn.edu/grouperWs/servicesRest/4.9.3/subjects/{request.user.pennid}/groups"
        response = requests.get(url, auth=(PENN_GROUPS_USER, PENN_GROUPS_PWD))
        return JsonResponse(response.json(), status=HTTPStatus.OK)
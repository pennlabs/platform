import requests

from django.conf import settings
from django.http.response import HttpResponse
from django.views.generic.base import View


PRODUCTS_TO_URL = {
    "website": "pennlabs.org/",
    "platform": "platform.pennlabs.org/",
    "penn-clubs": "pennclubs.com/",
}


class PullsView(View):
    """
    Returns a view displaying all PRs that have the feature-branch tag.

    """

    def get(self, request):
        headers = {"Authorization": settings.GH_PERSONAL_ACCESS_TOKEN}
        pulls = []

        for product, product_url in PRODUCTS_TO_URL.items():
            url = f"https://api.github.com/repos/pennlabs/{product}/pulls"
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                print(f"Error: Request returned status code {r.status_code}")
                return

            for pull in r.json():
                if "labels" not in pull:
                    continue
                for label in pull["labels"]:
                    if "name" in label and label["name"] == "dependencies":
                        # if "name" in label and label["name"].startswith("feature-branch:"):
                        pulls.append(
                            {
                                "url": f"https://pr-{pull['number']}.{product_url}",
                                "status": "STATUS"
                                # "status": label["name"].split(":")[1]
                            }
                        )
                        break
        return HttpResponse("<br>".join(str(pull) for pull in pulls))

import base64
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from oauth2_provider.models import (
    get_access_token_model,
    get_application_model,
    get_refresh_token_model,
)


def refresh_lifetime(seconds):
    return override_settings(
        OAUTH2_PROVIDER={
            **settings.OAUTH2_PROVIDER,
            "REFRESH_TOKEN_EXPIRE_SECONDS": seconds,
        }
    )


class RefreshTokenLifetimeTestCase(TestCase):
    def setUp(self):
        self.AccessToken = get_access_token_model()
        self.RefreshToken = get_refresh_token_model()
        Application = get_application_model()
        self.user = get_user_model().objects.create_user(
            pennid=10000001, username="bfranklin"
        )
        self.application = Application.objects.create(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            client_secret="secret",
        )
        self.credentials = base64.b64encode(
            f"{self.application.client_id}:secret".encode("utf-8")
        ).decode("utf-8")

    def create_refresh_token(self, age):
        access = self.AccessToken.objects.create(
            user=self.user,
            token="old-access",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(hours=1),
            scope="read",
        )
        refresh = self.RefreshToken.objects.create(
            user=self.user,
            token="old-refresh",
            application=self.application,
            access_token=access,
        )
        # created is auto_now_add
        self.RefreshToken.objects.filter(pk=refresh.pk).update(
            created=timezone.now() - age
        )
        return refresh.token

    def refresh(self, token):
        return self.client.post(
            reverse("oauth2_provider:token"),
            {"grant_type": "refresh_token", "refresh_token": token},
            HTTP_AUTHORIZATION=f"Basic {self.credentials}",
        )

    @refresh_lifetime(None)
    def test_no_lifetime(self):
        token = self.create_refresh_token(datetime.timedelta(days=365))
        self.assertEqual(200, self.refresh(token).status_code)

    @refresh_lifetime(3600)
    def test_within_lifetime(self):
        token = self.create_refresh_token(datetime.timedelta(minutes=30))
        self.assertEqual(200, self.refresh(token).status_code)

    @refresh_lifetime(3600)
    def test_expired(self):
        token = self.create_refresh_token(datetime.timedelta(hours=2))
        response = self.refresh(token)
        self.assertEqual(400, response.status_code)
        self.assertEqual("invalid_grant", response.json()["error"])

    @refresh_lifetime(3600)
    def test_refreshing_restarts_lifetime(self):
        token = self.create_refresh_token(datetime.timedelta(minutes=59))
        response = self.refresh(token)
        self.assertEqual(200, response.status_code)
        new_token = self.RefreshToken.objects.get(
            token=response.json()["refresh_token"]
        )
        self.assertAlmostEqual(
            timezone.now().timestamp(), new_token.created.timestamp(), delta=5
        )

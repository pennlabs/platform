import base64
import datetime
import json
import time

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from jwcrypto import jwk, jwt
from oauth2_provider.models import (
    get_access_token_model,
    get_application_model,
    get_refresh_token_model,
)
from oauthlib.common import Request

from accounts.jwt_tokens import generate_access_token
from accounts.models import Email
from accounts.serializers import UserSerializer


AUDIENCE = "urn:pennlabs:api"


class JWTAccessTokenTestCase(TestCase):
    def setUp(self):
        self.Application = get_application_model()
        self.AccessToken = get_access_token_model()
        self.RefreshToken = get_refresh_token_model()
        self.user = get_user_model().objects.create_user(
            pennid=10000001,
            username="bfranklin",
            first_name="Benjamin",
            last_name="Franklin",
        )
        Email.objects.create(
            user=self.user, value="bfranklin@upenn.edu", primary=True, verified=True
        )
        self.user.groups.add(Group.objects.create(name="student"))
        self.user.user_permissions.add(Permission.objects.get(codename="add_user"))
        self.application = self.Application.objects.create(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=self.Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=self.Application.GRANT_AUTHORIZATION_CODE,
            client_secret="secret",
        )

    def oauthlib_request(self, user):
        request = Request(
            "http://testserver/accounts/token/", headers={"HTTP_HOST": "testserver"}
        )
        request.user = user
        request.client = self.application
        request.scopes = ["read", "introspection"]
        request.expires_in = 600
        return request

    def refresh(self):
        access = self.AccessToken.objects.create(
            user=self.user,
            token="old-access",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(hours=1),
            scope="read introspection",
        )
        self.RefreshToken.objects.create(
            user=self.user,
            token="old-refresh",
            application=self.application,
            access_token=access,
        )
        credentials = base64.b64encode(
            f"{self.application.client_id}:secret".encode("utf-8")
        ).decode("utf-8")
        response = self.client.post(
            reverse("oauth2_provider:token"),
            {"grant_type": "refresh_token", "refresh_token": "old-refresh"},
            HTTP_AUTHORIZATION=f"Basic {credentials}",
        )
        self.assertEqual(response.status_code, 200, response.content)
        return response.json()

    def verify(self, token):
        """
        Verify like a product backend: with the published JWKS key named by the kid
        """
        header = json.loads(base64.urlsafe_b64decode(token.split(".")[0] + "=="))
        jwks = jwk.JWKSet.from_json(
            self.client.get(reverse("oauth2_provider:oidc-jwks-info")).content
        )
        key = jwks.get_key(header["kid"])
        self.assertIsNotNone(key, "token's kid is not in the published JWKS")
        verified = jwt.JWT(
            key=key,
            jwt=token,
            algs=["RS256"],
            check_claims={"aud": AUDIENCE, "exp": None},
        )
        return header, json.loads(verified.claims)

    def test_flag_off_issues_opaque_token(self):
        token = generate_access_token(self.oauthlib_request(self.user))
        self.assertNotIn(".", token)
        self.assertLess(len(token), 255)

    @override_settings(JWT_ACCESS_TOKENS_ENABLED=True)
    def test_claims(self):
        before = int(time.time())
        token = generate_access_token(self.oauthlib_request(self.user))
        header, claims = self.verify(token)
        self.assertEqual("at+jwt", header["typ"])
        self.assertEqual("http://testserver/accounts", claims["iss"])
        self.assertEqual("10000001", claims["sub"])
        self.assertEqual(AUDIENCE, claims["aud"])
        self.assertGreaterEqual(claims["iat"], before)
        self.assertEqual(claims["iat"] + 600, claims["exp"])
        self.assertEqual(self.application.client_id, claims["client_id"])
        self.assertEqual("read introspection", claims["scope"])
        self.assertEqual("access", claims["use"])

    @override_settings(JWT_ACCESS_TOKENS_ENABLED=True)
    def test_user_claims_match_introspection(self):
        _, claims = self.verify(generate_access_token(self.oauthlib_request(self.user)))
        introspected = UserSerializer(self.user).data
        # the fields django-labs-accounts syncs from introspection
        for field in [
            "pennid",
            "username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "user_permissions",
        ]:
            self.assertEqual(introspected[field], claims[field], field)

    @override_settings(JWT_ACCESS_TOKENS_ENABLED=True)
    def test_unique_jti(self):
        _, first = self.verify(generate_access_token(self.oauthlib_request(self.user)))
        _, second = self.verify(generate_access_token(self.oauthlib_request(self.user)))
        self.assertNotEqual(first["jti"], second["jti"])

    @override_settings(JWT_ACCESS_TOKENS_ENABLED=True)
    def test_token_without_user_stays_opaque(self):
        token = generate_access_token(self.oauthlib_request(None))
        self.assertNotIn(".", token)

    def test_refresh_flag_off(self):
        tokens = self.refresh()
        self.assertNotIn(".", tokens["access_token"])

    @override_settings(JWT_ACCESS_TOKENS_ENABLED=True)
    def test_refresh_issues_jwt_access_and_opaque_refresh_token(self):
        tokens = self.refresh()
        _, claims = self.verify(tokens["access_token"])
        self.assertEqual("10000001", claims["sub"])
        self.assertEqual(tokens["expires_in"], claims["exp"] - claims["iat"])
        self.assertNotIn(".", tokens["refresh_token"])
        stored = self.AccessToken.objects.get(token=tokens["access_token"])
        self.assertAlmostEqual(stored.expires.timestamp(), claims["exp"], delta=5)

    @override_settings(JWT_ACCESS_TOKENS_ENABLED=True)
    def test_jwt_still_introspects(self):
        tokens = self.refresh()
        resource_server = self.AccessToken.objects.create(
            user=self.user,
            token="resource-server",
            application=self.application,
            expires=timezone.now() + datetime.timedelta(hours=1),
            scope="introspection",
        )
        response = self.client.post(
            reverse("oauth2_provider:introspect"),
            {"token": tokens["access_token"]},
            HTTP_AUTHORIZATION=f"Bearer {resource_server.token}",
        )
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertTrue(content["active"])
        self.assertEqual(10000001, content["user"]["pennid"])

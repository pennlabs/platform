import json
import time
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from identity.views import SIGNING_ALG
from jwcrypto import jwk, jwt
from oauth2_provider.models import get_application_model


class AttestTestCase(TestCase):
    def setUp(self):
        self.key = jwk.JWK.from_pem(settings.IDENTITY_RSA_PRIVATE_KEY.encode("utf-8"))
        self.client = Client()
        self.Application = get_application_model()
        self.UserModel = get_user_model()
        self.test_user = self.UserModel.objects.create_user(
            pennid=2, username="bar_user"
        )

        self.application = self.Application(
            name="Test Application",
            redirect_uris="http://localhost http://example.com http://example.org",
            user=self.test_user,
            client_type=self.Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=self.Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

    # def test_valid_attest(self):
    #     app = self.application
    #     auth_encoded = base64.b64encode(
    #         f"{app.client_id}:{app.client_secret}".encode("utf-8")
    #     )
    #     auth_headers = {
    #         "HTTP_AUTHORIZATION": f"Basic {auth_encoded.decode('utf-8')}",
    #     }
    #     response = self.client.post(reverse("identity:attest"), **auth_headers)
    #     content = response.json()
    #     self.assertIsInstance(content, dict)
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     expected_urn = "urn:pennlabs:test-application"
    #     access_jwt = jwt.JWT(key=self.key, jwt=content["access"])
    #     refresh_jwt = jwt.JWT(key=self.key, jwt=content["refresh"])
    #     access_claims = json.loads(access_jwt.claims)
    #     refresh_claims = json.loads(refresh_jwt.claims)
    #     self.assertEqual(expected_urn, access_claims["sub"])
    #     self.assertEqual(expected_urn, refresh_claims["sub"])
    #     self.assertEqual("access", access_claims["use"])
    #     self.assertEqual("refresh", refresh_claims["use"])
    #     now = time.time()
    #     self.assertLessEqual(access_claims["iat"], now)
    #     self.assertLessEqual(refresh_claims["iat"], now)
    #     self.assertGreaterEqual(access_claims["exp"], now)
    #     self.assertNotIn("exp", refresh_claims)

    def test_bad_secret(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Basic worniuvoasnlksdfjlksjdflk",
        }
        response = self.client.post(reverse("identity:attest"), **auth_headers)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertNotIn("access", content)
        self.assertNotIn("refresh", content)

    def test_no_auth(self):
        auth_headers = {}
        response = self.client.post(reverse("identity:attest"), **auth_headers)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertNotIn("access", content)
        self.assertNotIn("refresh", content)


class JwksTestCase(TestCase):
    def setUp(self):
        self.key = jwk.JWK.from_pem(settings.IDENTITY_RSA_PRIVATE_KEY.encode("utf-8"))
        self.client = Client()

    def test_jwks(self):
        response = self.client.get(reverse("identity:jwks"))
        content = response.json()
        self.assertIsInstance(content, dict)
        found_key = jwk.JWK.from_json(json.dumps(content["keys"][0]))
        self.assertEqual(self.key.thumbprint(), found_key.thumbprint())
        self.assertEqual(self.key.key_id, found_key.key_id)
        self.assertEqual(self.key.key_type, found_key.key_type)
        self.assertTrue(found_key.has_public)
        self.assertFalse(found_key.has_private)


class RefreshTestCase(TestCase):
    def setUp(self):
        self.key = jwk.JWK.from_pem(settings.IDENTITY_RSA_PRIVATE_KEY.encode("utf-8"))
        self.client = Client()
        self.urn = "urn:random:product"

    def test_valid_refresh(self):
        now = time.time()
        token = jwt.JWT(
            header={"alg": SIGNING_ALG},
            claims={"sub": self.urn, "use": "refresh", "iat": now},
        )
        token.make_signed_token(self.key)
        auth_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {token.serialize()}",
        }
        response = self.client.post(reverse("identity:refresh"), **auth_headers)
        content = response.json()
        self.assertIsInstance(content, dict)
        found_access = jwt.JWT(key=self.key, jwt=content["access"])
        access_claims = json.loads(found_access.claims)
        self.assertEqual(self.urn, access_claims["sub"])
        self.assertEqual("access", access_claims["use"])
        now = time.time()
        self.assertLessEqual(access_claims["iat"], now)
        self.assertGreaterEqual(access_claims["exp"], now)

    def test_refresh_with_access(self):
        now = time.time()
        token = jwt.JWT(
            header={"alg": SIGNING_ALG},
            claims={"sub": self.urn, "use": "access", "iat": now},
        )
        token.make_signed_token(self.key)
        auth_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {token.serialize()}",
        }
        response = self.client.post(reverse("identity:refresh"), **auth_headers)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertNotIn("access", content)

    def test_refresh_no_use(self):
        now = time.time()
        token = jwt.JWT(
            header={"alg": SIGNING_ALG}, claims={"sub": self.urn, "iat": now}
        )
        token.make_signed_token(self.key)
        auth_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {token.serialize()}",
        }
        response = self.client.post(reverse("identity:refresh"), **auth_headers)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertNotIn("access", content)

    def test_unauthenticated(self):
        response = self.client.post(reverse("identity:refresh"))
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
        self.assertNotIn("access", content)

    def test_incomplete_bearer(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer",
        }
        response = self.client.post(reverse("identity:refresh"), **auth_headers)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
        self.assertNotIn("access", content)

    def test_garbage_bearer(self):
        auth_headers = {
            "HTTP_AUTHORIZATION": "Bearer abc123",
        }
        response = self.client.post(reverse("identity:refresh"), **auth_headers)
        content = response.json()
        self.assertIsInstance(content, dict)
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertNotIn("access", content)


class HealthTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health(self):
        url = reverse("healthbackend:health")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"message": "OK"})

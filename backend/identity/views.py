import json
from http import HTTPStatus

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from identity.utils import (
    ID_PRIVATE_KEY,
    SIGNING_ALG,
    mint_access_jwt,
    mint_refresh_jwt,
)
from jwcrypto import jwt
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin


@method_decorator(csrf_exempt, name="dispatch")
class AttestView(OAuthLibMixin, View):
    """
    Implements an endpoint to attest with client id + client secret

    This endpoint returns a refresh JWT with an unlimited lifetime and an access JWT with
    a short lifetime.
    """

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request, *args, **kwargs):
        request.client = None

        # Taken from https://github.com/jazzband/django-oauth-toolkit/blob/41aa49e6d7fad0a392b1557d1ef6d40ccc444f7e/oauth2_provider/oauth2_backends.py#L178 # noqa
        # Normally would use self.authenticate_client(), however since that constructs
        # a new request object, we don't gain access to the underlying client.
        self.request.headers = self.get_oauthlib_core().extract_headers(self.request)
        authenticated = self.get_server().request_validator.authenticate_client(
            request, *args, **kwargs
        )
        if not authenticated:
            return JsonResponse(
                data={"detail": "Missing or invalid credentials."},
                status=HTTPStatus.UNAUTHORIZED,
            )

        # pulls out name as recorded in DOT application database
        local_name = slugify(request.client.name)
        # example urn: `urn:pennlabs:platform`
        urn = f"urn:pennlabs:{local_name}"
        return JsonResponse(
            data={
                "access": mint_access_jwt(ID_PRIVATE_KEY, urn).serialize(),
                "refresh": mint_refresh_jwt(ID_PRIVATE_KEY, urn).serialize(),
            }
        )


class JwksInfoView(View):
    """
    View used to show json web key set document

    Largely copied from the Django Oauth Toolkit implementation:
    https://github.com/jazzband/django-oauth-toolkit/blob/4655c030be15616ba6e0872253a2c15a897d9701/oauth2_provider/views/oidc.py#L61  # noqa
    """

    # building out JWKS view at init time so we don't have to recalculate it for each request
    def __init__(self, **kwargs):
        data = {
            "keys": [
                {"alg": SIGNING_ALG, "use": "sig", "kid": ID_PRIVATE_KEY.thumbprint()}
            ]
        }
        data["keys"][0].update(json.loads(ID_PRIVATE_KEY.export_public()))
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        self.jwks_response = response

        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return self.jwks_response


@method_decorator(csrf_exempt, name="dispatch")
class RefreshJWTView(View):
    """
    View used for refreshing access JWTs
    """

    def post(self, request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header is None:
            return JsonResponse(
                data={"detail": "Authentication credentials were not provided."},
                status=HTTPStatus.UNAUTHORIZED,
            )
        split_header = auth_header.split(" ")
        if len(split_header) < 2 or split_header[0] != "Bearer":
            return JsonResponse(
                data={"detail": "No Bearer token present in Authorization header."},
                status=HTTPStatus.UNAUTHORIZED,
            )
        try:
            # this line will decode and validate the JWT, raising an exception for
            # anything that cannot be decoded or validated
            refresh_jwt = jwt.JWT(key=ID_PRIVATE_KEY, jwt=split_header[1])
            claims = json.loads(refresh_jwt.claims)
            if "use" not in claims or claims["use"] != "refresh":
                return JsonResponse(
                    data={"detail": "Invalid JWT. Must provide a valid refresh JWT."},
                    status=HTTPStatus.BAD_REQUEST,
                )
            urn = claims["sub"]
            new_access_jwt = mint_access_jwt(ID_PRIVATE_KEY, urn)
            return JsonResponse(data={"access": new_access_jwt.serialize()})
        except Exception as e:
            return JsonResponse(
                data={"detail": f"Invalid JWT: {e}"},
                status=HTTPStatus.BAD_REQUEST,
            )

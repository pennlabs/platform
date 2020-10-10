import json
from http import HTTPStatus

from django.conf import settings
from django.http import JsonResponse
from django.utils.text import slugify
from django.views.generic import View
from identity.utils import SIGNING_ALG, mint_access_jwt, mint_refresh_jwt
from jwcrypto import jwk, jwt
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin


id_privkey = jwk.JWK.from_pem(settings.IDENTITY_RSA_PRIVATE_KEY.encode("utf-8"))


class AttestView(OAuthLibMixin, View):
    """
    Implements an endpoint to attest with client id + client secret

    This endpoint returns a refresh JWT with an unlimited lifetime and an access JWT with
    a short lifetime.
    """

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def __init__(self, **kwargs):
        self.validator = self.get_validator_class()()
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        request.client = None
        authenticated = self.validator.authenticate_client(request, *args, **kwargs)
        if not authenticated:
            return JsonResponse(data={"error": "unauthenticated"}, status=HTTPStatus.UNAUTHORIZED)

        # pulls out name as recorded in DOT application database
        local_name = slugify(request.client.name)
        # example urn: `urn:pennlabs.org:ohq`
        urn = f"urn:pennlabs.org:{local_name}"
        return JsonResponse(
            data={
                "access": mint_access_jwt(id_privkey, urn).serialize(),
                "refresh": mint_refresh_jwt(id_privkey, urn).serialize(),
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
        data = {"keys": [{"alg": SIGNING_ALG, "use": "sig", "kid": id_privkey.thumbprint()}]}
        data["keys"][0].update(json.loads(id_privkey.export_public()))
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        self.jwks_response = response

        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return self.jwks_response


class RefreshJWTView(View):
    """
    View used for refreshing access JWTs
    """

    def get(self, request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header is None:
            return JsonResponse(
                data={"error": "no authorization provided"}, status=HTTPStatus.UNAUTHORIZED,
            )
        split_header = auth_header.split(" ")
        if len(split_header) < 2 or split_header[0] != "Bearer":
            return JsonResponse(
                data={"error": "please provide authorization with bearer token"},
                status=HTTPStatus.UNAUTHORIZED,
            )
        try:
            refresh_jwt = jwt.JWT(key=id_privkey, jwt=split_header[1])
            claims = json.loads(refresh_jwt.claims)
            if "use" not in claims or claims["use"] != "refresh":
                raise Exception("expected JWT with `use -> refresh` claim")
            urn = claims["sub"]
            new_access_jwt = mint_access_jwt(id_privkey, urn)
            return JsonResponse(data={"access": new_access_jwt.serialize()})
        except Exception as e:
            return JsonResponse(
                data={"error": f"failure validating refresh jwt: {e}"},
                status=HTTPStatus.BAD_REQUEST,
            )

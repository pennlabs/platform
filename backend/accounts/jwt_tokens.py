import time
import uuid
from functools import lru_cache

from django.conf import settings
from jwcrypto import jwk, jwt
from oauth2_provider.settings import oauth2_settings
from oauthlib.oauth2.rfc6749.tokens import random_token_generator


SIGNING_ALG = "RS256"


@lru_cache(maxsize=None)
def get_signing_key() -> jwk.JWK:
    """
    The OIDC key, whose public half DOT already publishes at /accounts/.well-known/jwks.json
    """
    return jwk.JWK.from_pem(oauth2_settings.OIDC_RSA_PRIVATE_KEY.encode("utf-8"))


def get_access_token_claims(request) -> dict:
    """
    RFC 9068 access token claims, plus the user fields django-labs-accounts reads
    from /accounts/introspect/, under the same names
    """
    user = request.user
    now = int(time.time())
    return {
        "iss": oauth2_settings.oidc_issuer(request),
        "sub": str(user.pennid),
        "aud": settings.JWT_ACCESS_TOKEN_AUDIENCE,
        "iat": now,
        "exp": now + int(request.expires_in),
        "jti": uuid.uuid4().hex,
        "client_id": request.client.client_id,
        "scope": " ".join(request.scopes),
        "use": "access",
        "pennid": user.pennid,
        "username": user.username,
        "first_name": user.get_preferred_name(),
        "last_name": user.last_name,
        "email": user.get_email(),
        "groups": sorted(user.groups.values_list("name", flat=True)),
        "user_permissions": sorted(
            user.user_permissions.values_list("codename", flat=True)
        ),
    }


def generate_access_token(request) -> str:
    """
    Signed JWT when JWT_ACCESS_TOKENS_ENABLED is on; otherwise, and for tokens with
    no user (client credentials), the usual opaque token
    """
    if not settings.JWT_ACCESS_TOKENS_ENABLED or getattr(request, "user", None) is None:
        return random_token_generator(request)
    key = get_signing_key()
    token = jwt.JWT(
        header={"alg": SIGNING_ALG, "typ": "at+jwt", "kid": key.thumbprint()},
        claims=get_access_token_claims(request),
    )
    token.make_signed_token(key)
    return token.serialize()

import time

from django.conf import settings
from jwcrypto import jwk, jwt


SIGNING_ALG = "RS256"
EXPIRY_TIME = 15 * 60  # 15 minutes
ID_PRIVATE_KEY = jwk.JWK.from_pem(settings.IDENTITY_RSA_PRIVATE_KEY.encode("utf-8"))


def mint_access_jwt(key: jwk.JWK, urn: str) -> jwt.JWT:
    """
    Mint a JWT with the following claims:
    - use -> access - this says that this JWT is strictly an access JWT
    - iat -> now - this says that this JWT isn't active until the current time.
    this protects us from attacks from clock skew
    - exp -> expiry_time - this makes sure our JWT is only valid for EXPIRY_TIME
    """
    now = time.time()
    expiry_time = now + EXPIRY_TIME
    token = jwt.JWT(
        header={"alg": SIGNING_ALG},
        claims={"sub": urn, "use": "access", "iat": now, "exp": expiry_time},
    )
    token.make_signed_token(key)
    return token


def mint_refresh_jwt(key: jwk.JWK, urn: str) -> jwt.JWT:
    """
    Mint a JWT with the following claims:
    - use -> refresh - this says that this JWT is strictly a refresh JWT
    - iat -> now - this says that this JWT isn't active until the current time.
      this protects us from attacks from clock skew
    - no exp claim because refresh JWTs do not expire
    """
    now = time.time()
    token = jwt.JWT(header={"alg": SIGNING_ALG}, claims={"sub": urn, "use": "refresh", "iat": now})
    token.make_signed_token(key)
    return token

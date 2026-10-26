from datetime import timedelta

from django.utils import timezone
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.settings import oauth2_settings


class LabsOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = OAuth2Validator.oidc_claim_scope
    oidc_claim_scope.update(
        {
            "name": "read",
            "email": "read",
            "pennkey": "read",
            "pennid": "read",
            "is_staff": "read",
            "is_active": "read",
        }
    )

    def get_additional_claims(self, request):
        return {
            "name": request.user.preferred_name or request.user.get_full_name(),
            "email": request.user.get_email(),
            "pennkey": request.user.username,
            "pennid": request.user.pennid,
            "is_staff": request.user.is_staff,
            "is_active": request.user.is_active,
        }

    def validate_refresh_token(self, refresh_token, client, request, *args, **kwargs):
        """
        DOT only applies REFRESH_TOKEN_EXPIRE_SECONDS in cleartokens, so check it here too
        """
        if not super().validate_refresh_token(
            refresh_token, client, request, *args, **kwargs
        ):
            return False
        lifetime = oauth2_settings.REFRESH_TOKEN_EXPIRE_SECONDS
        if lifetime is None:
            return True
        return request.refresh_token_instance.created > timezone.now() - timedelta(
            seconds=lifetime
        )

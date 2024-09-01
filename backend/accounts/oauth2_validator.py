from oauth2_provider.oauth2_validators import OAuth2Validator


class LabsOAuth2Validator(OAuth2Validator):
    oidc_claim_scope = OAuth2Validator.oidc_claim_scope
    oidc_claim_scope.update({"name": "read",
                             "email": "read",
                             "pennid": "read",
                             "is_staff": "read",
                             "is_active": "read"})
    
    def get_additional_claims(self, request):
        return {
            "name": request.user.preferred_name or
            request.user.get_full_name(),
            "email": request.user.email,
            "pennid": request.user.pennid,
            "is_staff": request.user.is_staff,
            "is_active": request.user.is_active,
        }

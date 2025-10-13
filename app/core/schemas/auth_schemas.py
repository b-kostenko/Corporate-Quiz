import secrets
from urllib.parse import urlencode

from pydantic import BaseModel


class AzureAuthorizationResponse(BaseModel):
    """Azure OAuth2 URL parameters."""
    authorization_endpoint: str
    client_id: str
    response_type: str = "code"
    redirect_uri: str
    response_mode: str = "query"
    scope: str
    nonce: str
    state: str

    class Config:
        extra = "forbid"

    def generate_url(self) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": self.response_type,
            "redirect_uri": self.redirect_uri,
            "response_mode": self.response_mode,
            "scope": self.scope,
            "nonce": self.nonce,
            "state": self.state
        }
        return f"{self.authorization_endpoint}/common/oauth2/authorize?{urlencode(params)}"

    @staticmethod
    def generate_state() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def generate_nonce() -> str:
        return secrets.token_urlsafe(16)


class SSOTokensResponse(BaseModel):
    """SSO tokens response schema."""
    access_token: str
    expires_in: int
    id_token: str
    scope: str
    token_type: str

class GoogleAuthorizationResponse(BaseModel):
    """Google OAuth2/OIDC URL parameters."""
    authorization_endpoint: str
    client_id: str
    response_type: str = "code"
    redirect_uri: str
    response_mode: str = "query"
    scope: str
    state: str
    nonce: str
    prompt: str | None = "consent"

    class Config:
        extra = "forbid"

    def generate_url(self) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": self.response_type,
            "redirect_uri": self.redirect_uri,
            "response_mode": self.response_mode,
            "scope": self.scope,
            "state": self.state,
            "nonce": self.nonce,
        }
        if self.prompt:
            params["prompt"] = self.prompt

        return f"{self.authorization_endpoint}/o/oauth2/v2/auth?{urlencode(params)}"

    @staticmethod
    def generate_state() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def generate_nonce() -> str:
        return secrets.token_urlsafe(16)
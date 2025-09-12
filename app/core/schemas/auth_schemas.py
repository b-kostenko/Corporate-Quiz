import secrets
from urllib.parse import urlencode

from pydantic import BaseModel


class AzureAuthorizationResponse(BaseModel):
    """Azure OAuth2 URL parameters."""
    authorization_endpoint: str
    client_id: str
    response_type: str = "id_token"
    redirect_uri: str
    response_mode: str = "form_post"
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


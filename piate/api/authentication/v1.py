from dataclasses import dataclass
from typing import List, Dict, NewType

from dataclasses_json import dataclass_json, Undefined

from piate.api.authentication import (
    AuthenticationBase,
    RefreshToken,
    ExpirationBase,
)
from piate.api.version import APIVersion

AuthToken = NewType("AuthToken", str)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class TokenResponse:
    """Response from the Authentication API"""

    token_type: str
    tokens: List[AuthToken]
    refresh_token: RefreshToken
    permission_name_by_id: Dict[str, str]
    role_group_name_by_id: Dict[str, str]
    expiration: ExpirationBase


class Authentication(AuthenticationBase):
    API_VERSION = APIVersion.V1

    def token(self, base_url: str, username: str, password: str) -> TokenResponse:
        return TokenResponse.from_dict(
            super().token(base_url=base_url, username=username, password=password)
        )

    def extends(self, base_url: str, refresh_token: str) -> TokenResponse:
        return TokenResponse.from_dict(
            super().extends(base_url=base_url, refresh_token=refresh_token)
        )

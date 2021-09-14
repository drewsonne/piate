from dataclasses import dataclass
from datetime import datetime
from typing import NewType, List

from dataclasses_json import dataclass_json, Undefined

from piate.api.authentication.base import (
    AuthenticationBase,
    RefreshToken,
    ExpirationBase,
)
from piate.api.version import APIVersion

IDToken = NewType("IDToken", str)
AccessToken = NewType("AccessToken", str)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Expiration(ExpirationBase):
    id: datetime

    def id_expired(self) -> bool:
        return self.id >= datetime.now()


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class TokenResponseToken:
    id_token: IDToken
    access_token: AccessToken


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class TokenResponse:
    token_type: str
    refresh_token: RefreshToken
    tokens: List[TokenResponseToken]
    expiration: Expiration


class Authentication(AuthenticationBase):
    API_VERSION = APIVersion.V2

    def token(self, base_url: str, username: str, password: str) -> TokenResponse:
        return TokenResponse.from_dict(
            super().token(base_url=base_url, username=username, password=password)
        )

    def extends(self, base_url: str, refresh_token: RefreshToken) -> TokenResponse:
        return TokenResponse.from_dict(
            super().extends(base_url=base_url, refresh_token=refresh_token)
        )

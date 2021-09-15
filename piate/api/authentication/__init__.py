from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, NewType
from datetime import datetime, timedelta

import requests
from dataclasses_json import dataclass_json, Undefined

from piate.api.version import APIVersion

RefreshToken = NewType("RefreshToken", str)


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class ExpirationBase:
    access: datetime
    refresh: datetime

    def access_expired(self) -> bool:
        return self.access >= datetime.now()

    def refresh_expired(self) -> bool:
        return self.refresh >= datetime.now()


class AuthenticationBase:
    PATH = "/oauth2/token"
    TOKEN_GRANT_TYPE = "password"
    EXTENDS_GRANT_TYPE = "refresh_token"
    API_VERSION: APIVersion

    def _generate_expiration(self) -> Dict:
        now = datetime.now()
        expiration = {
            "access": now + timedelta(hours=3),
            "refresh": now + timedelta(hours=12),
        }
        if self.API_VERSION == APIVersion.V2:
            expiration["id"] = now + timedelta(hours=3)
        return expiration

    @abstractmethod
    def token(self, base_url: str, username: str, password: str) -> Dict:
        response = requests.post(
            f"{base_url}{self.PATH}",
            params={
                "grant_type": self.TOKEN_GRANT_TYPE,
                "username": username,
                "password": password,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": f"application/vnd.iate.token+json; version={self.API_VERSION.value}",
            },
        ).json()

        response["expiration"] = self._generate_expiration()
        return response

    @abstractmethod
    def extends(self, base_url: str, refresh_token: str) -> Dict:
        response = requests.post(
            f"{base_url}{self.PATH}",
            paarams={
                "grant_type": self.EXTENDS_GRANT_TYPE,
                "refresh_token": refresh_token,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": f"application/vnd.iate.token+json; version={self.API_VERSION.value}",
            },
        ).json()

        response["expiration"] = self._generate_expiration()
        return response

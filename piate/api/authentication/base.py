from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, NewType
from datetime import datetime, timedelta

import requests
from dataclasses_json import dataclass_json

RefreshToken = NewType("RefreshToken", str)


class AuthenticationVersion(Enum):
    V1 = "1"
    V2 = "2"


@dataclass_json
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
    API_VERSION: AuthenticationVersion

    def _generate_expiration(self) -> Dict:
        now = datetime.now()
        expiration = {
            "access": now + timedelta(hours=3),
            "refresh": now + timedelta(hours=12),
        }
        if self.API_VERSION == AuthenticationVersion.V2:
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

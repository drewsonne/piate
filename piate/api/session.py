import json
from typing import Optional, Dict, Any, Union

import requests

from piate.api.version import APIVersion
from piate.api.authentication.v2 import Authentication, TokenResponse
from piate.api.credentials import Credentials
from piate.api.response import MetadataResource


class Session:
    BASE_URL: str = "https://iate.europa.eu/em-api"

    _credentials: Optional[TokenResponse]
    _http_session: requests.Session

    def __init__(self, credentials: Credentials):
        self._http_session = requests.Session()

        self._oauth_client = Authentication()

        self._username = credentials.username
        self._api_key = credentials.api_key

        self._credentials = None

    @property
    def credentials(self) -> TokenResponse:
        if self._credentials is None:
            self._credentials = self._oauth_client.token(
                base_url=self.BASE_URL, username=self._username, password=self._api_key
            )
        if self._credentials.expiration.access_expired():
            if not self._credentials.expiration.refresh_expired():
                self._credentials = self._oauth_client.extends(
                    base_url=self.BASE_URL,
                    refresh_token=self._credentials.refresh_token,
                )
            else:
                self._credentials = self._oauth_client.token(
                    base_url=self.BASE_URL,
                    username=self._username,
                    password=self._api_key,
                )
        return self._credentials

    def get_metadata_resource(self, resource: MetadataResource) -> Dict:

        api_versions = resource.get_acceptable_api_versions()
        version = api_versions[0]

        response = self._http_session.get(
            resource.href, headers={"Accept": APIVersion.to_mimetype(version)}
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def get(
        self,
        path: str,
        params: Dict[str, Union[int, str]],
        version: APIVersion,
        do_auth: bool = True,
    ) -> Dict:

        if do_auth:
            raise NotImplementedError()
        else:
            response = self._http_session.get(
                f"{self.BASE_URL}{path}",
                params=params,
                headers={
                    "Accept": f"application/vnd.iate.collection+json;version={1 if version == APIVersion.V1 else 2}"
                },
            )
            if not response.ok:
                response.raise_for_status()

            return response.json()

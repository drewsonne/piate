from typing import Optional

from piate.api.client import Client
from piate.api.credentials import Credentials

from piate.api.resources.inventories import Inventories
from piate.api.session import Session


class MissingAuthentication(Exception):
    def __init__(self):
        super().__init__(
            "Either a 'session' object or a 'username' and 'api_key' must be provided."
        )


def client(
    username: Optional[str] = None,
    api_key: Optional[str] = None,
    session: Optional[Session] = None,
):
    has_login = (username is not None) and (api_key is not None)
    has_session = session is None
    if not has_session:
        if has_login:
            session = Session(Credentials(username=username, api_key=api_key))
        else:
            raise MissingAuthentication()
    return Client(session)


__all__ = ["client"]

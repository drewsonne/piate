from typing import Optional

# We use the longer paths here as PyCharm will suggest imports from here for other classes
from piate.api import client as client_mod, session as sessions, credentials, resources


class MissingAuthentication(Exception):
    """
    Raise when no authentication information is provided
    """

    def __init__(self):
        super().__init__(
            "Either a 'session' object or a 'username' and 'api_key' must be provided."
        )


def client(
    username: Optional[str] = None,
    api_key: Optional[str] = None,
    session: Optional[sessions.Session] = None,
):
    """
    Library entrypoint. If `username` and `api_key` (conflicts with `session`) are supplied they are used to
    authenticate against the API. If `session` (conflicts with `username` and `api_key`) is provided, it is used in
    place of `username` and `api_key`.
    """
    has_login = (username is not None) and (api_key is not None)
    has_session = session is None

    if not has_session:
        if has_login:
            session = sessions.Session(
                credentials.Credentials(username=username, api_key=api_key)
            )
        else:
            raise MissingAuthentication()
    return client_mod.Client(session)


__all__ = ["client"]

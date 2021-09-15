from piate.api.session import Session


class BaseResource:
    session: Session

    def __init__(self, session: Session):
        self.session = session

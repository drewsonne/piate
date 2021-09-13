from dataclasses import dataclass
from piate.api.session import Session


@dataclass(init=False)
class Inventories:
    def __init__(self, session: Session):
        self.session = session

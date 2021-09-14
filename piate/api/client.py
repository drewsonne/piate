from dataclasses import dataclass

from piate.api.resources.collections import Collections
from piate.api.resources.inventories import Inventories
from piate.api.session import Session


@dataclass(init=False)
class Client:
    inventories: Inventories
    collections: Collections

    def __init__(self, session: Session):
        self._session = session
        self.inventories = Inventories(self._session)
        self.collections = Collections(self._session)

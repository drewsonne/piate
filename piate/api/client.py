from dataclasses import dataclass

from piate.api.resources.collections import Collections
from piate.api.resources.domains import Domains
from piate.api.resources.institutions import Institutions
from piate.api.resources.inventories import Inventories
from piate.api.session import Session


@dataclass(init=False)
class Client:
    inventories: Inventories
    collections: Collections
    institutions: Institutions

    def __init__(self, session: Session):
        self._session = session

        self.inventories = Inventories(self._session)
        self.collections = Collections(self._session)
        self.domains = Domains(self._session)
        self.institutions = Institutions(self._session)

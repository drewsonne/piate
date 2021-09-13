from dataclasses import dataclass

from piate.api.resources.inventories import Inventories
from piate.api.session import Session


@dataclass(init=False)
class Client:
    inventories: Inventories

    def __init__(self, session: Session):
        self.session = session
        self.inventories = Inventories(self.session)

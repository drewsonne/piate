from dataclasses import dataclass

from piate.api.resources.inventories import Inventories


@dataclass
class Client:
    inventories: Inventories


def client(api_key: str):
    return Client(inventories=Inventories())


__all__ = ["client"]

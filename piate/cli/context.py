from dataclasses import dataclass

from piate.api.client import Client
from piate.cli.format import Format


@dataclass
class ContextObj:
    client: Client
    format: Format

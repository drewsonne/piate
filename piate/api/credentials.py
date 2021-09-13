from dataclasses import dataclass
from typing import Optional


@dataclass
class Credentials:
    username: Optional[str]
    api_key: Optional[str]

import re
from enum import Enum
from typing import Optional


class APIVersion(Enum):
    V1 = "1"
    V2 = "2"

    def __lt__(self, other: "APIVersion") -> bool:
        return int(self.value) < int(other.value)

    @classmethod
    def to_mimetype(cls, version: Optional["APIVersion"] = None) -> str:
        if version is None:
            return "application/json"
        return f"application/vnd.iate.collection+json;version={version.value}"

    @classmethod
    def from_mimetype(cls, mimetype: str) -> Optional["APIVersion"]:
        result = re.search(
            r"application/vnd.iate.collection\+json\;version=(\d+)", mimetype
        )
        if result is not None:
            return APIVersion(result.group(1))
        else:
            return None

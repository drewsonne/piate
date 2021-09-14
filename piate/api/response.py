from dataclasses import dataclass, field
from typing import TypeVar, List, Generic, Union, Optional

from dataclasses_json import dataclass_json

from piate.api.version import APIVersion

R = TypeVar("R")


@dataclass
class Link:
    href: str


@dataclass_json
@dataclass
class MetadataResource:
    href: str
    method: str
    accept_media_types: List[str]
    content_media_types: Optional[List[str]] = None

    def get_acceptable_api_versions(self) -> List[APIVersion]:
        mimetypes = [APIVersion.from_mimetype(m) for m in self.accept_media_types]
        fitlered_mimetypes = [m for m in mimetypes if m is not None]
        fitlered_mimetypes.sort(reverse=True)
        return fitlered_mimetypes


def create_paged_response_class(item_type):
    @dataclass_json
    @dataclass
    class PagedResponse:
        items: List[item_type]

        offset: int
        limit: int
        size: int

        self: MetadataResource
        create: MetadataResource
        search: MetadataResource
        next: Optional[MetadataResource] = field(default=None)

        def compact(self) -> item_type:
            return self.items

    return PagedResponse


@dataclass_json
@dataclass
class MetadataType:
    self: MetadataResource
    code: Union[int, str]
    name: str


@dataclass_json
@dataclass
class MetadataEditTimestamp:
    institution: MetadataType
    timestamp: str
    division: Optional[MetadataType] = None


@dataclass_json
@dataclass
class MetadataProtection:
    type: MetadataType


@dataclass_json
@dataclass
class Metadata:
    confidentiality: MetadataType
    creation: MetadataEditTimestamp
    modification: MetadataEditTimestamp
    protection: MetadataProtection

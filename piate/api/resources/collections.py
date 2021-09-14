from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import dataclass_json

from piate.api.version import APIVersion
from piate.api.response import (
    MetadataType,
    Metadata,
    MetadataResource,
    create_paged_response_class,
)
from piate.api.session import Session


@dataclass_json
@dataclass
class CollectionName:
    short_name: str
    full_name: str
    institution_code: Optional[str] = field(default=None)
    institution_name: Optional[str] = field(default=None)


@dataclass_json
@dataclass
class Collection:
    code: str
    id: int
    name: CollectionName
    description: str

    type: MetadataType
    metadata: Metadata
    self: MetadataResource
    update: MetadataResource
    delete: MetadataResource

    @dataclass_json
    @dataclass
    class Compact:
        code: str
        id: int
        name: CollectionName
        description: str

    def compact(self) -> Compact:
        return Collection.Compact(self.code, self.id, self.name, self.description)


CollectionPagedResponse = create_paged_response_class(Collection)


@dataclass(init=False)
class Collections:
    def __init__(self, session: Session):
        self.session = session

    def list_pages(self):
        page = self.list()
        yield page

        while page.next is not None:
            page = CollectionPagedResponse.from_dict(
                self.session.get_metadata_resource(page.next)
            )
            yield page

    def list(self) -> CollectionPagedResponse:
        response = self.session.get(
            "/collections",
            {"expand": "true", "offset": 0, "limit": 10},
            version=APIVersion.V2,
            do_auth=False,
        )
        return CollectionPagedResponse.from_dict(response)

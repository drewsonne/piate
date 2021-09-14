from dataclasses import dataclass

from dataclasses_json import dataclass_json

from piate.api.authentication.base import AuthenticationVersion
from piate.api.response import (
    MetadataType,
    Metadata,
    MetadataResource,
    create_response_class,
)
from piate.api.session import Session


@dataclass_json
@dataclass
class CollectionName:
    institution_code: str
    institution_name: str
    short_name: str
    full_name: str


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


CollectionPagedResponse = create_response_class(Collection)


@dataclass(init=False)
class Collections:
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> CollectionPagedResponse:
        response = self.session.get(
            "/collections",
            {"expand": "true", "offset": 0, "limit": 10},
            version=AuthenticationVersion.V2,
            do_auth=False,
        )
        return CollectionPagedResponse.from_dict(response)

from dataclasses import dataclass, field
from typing import Optional, Dict

from dataclasses_json import dataclass_json, Undefined

from piate.api.resources.base import BaseResource
from piate.api.response import (
    MetadataType,
    Metadata,
    MetadataResource,
    create_paged_response_class_v2,
)
from piate.api.version import APIVersion


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class CollectionNameLanguage:
    self: MetadataResource
    code: str
    name: str
    is_official: bool


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class CollectionName:
    short_name: str
    full_name: str

    year: Optional[int] = field(default=None)
    language: Optional[CollectionNameLanguage] = field(default=None)

    institution_code: Optional[str] = field(default=None)
    institution_name: Optional[str] = field(default=None)


@dataclass_json(undefined=Undefined.RAISE)
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

    def compact(self) -> Dict:
        return dict(
            code=self.code, id=self.id, name=self.name, description=self.description
        )


CollectionPagedResponse = create_paged_response_class_v2(Collection)


class Collections(BaseResource):
    def pages(self):
        page = self._first_page()
        yield page

        while page.next is not None:
            page = CollectionPagedResponse.from_dict(
                self.session.get_metadata_resource(page.next)
            )
            yield page

    def _first_page(self) -> CollectionPagedResponse:
        response = self.session.get(
            "/collections",
            {"expand": "true", "offset": 0, "limit": 10},
            version=APIVersion.V2,
            do_auth=False,
        )
        return CollectionPagedResponse.from_dict(response)

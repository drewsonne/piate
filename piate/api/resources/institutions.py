from dataclasses import dataclass, field
from typing import Optional, Dict

from dataclasses_json import dataclass_json, Undefined

from piate.api import API
from piate.api.resources.base import BaseResource
from piate.api.response import create_paged_response_class_generic, Meta


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class InstitutionMetadata:
    creation_date: str
    change_date: str


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Institution:
    meta: Meta
    code: str
    name: str
    metadata: InstitutionMetadata
    parent: Optional[str] = field(default=None)

    def compact(self) -> Dict:
        compact = {"code": self.code, "name": self.name, "metadata": self.metadata}
        if self.parent:
            compact["parent"] = self.parent

        return compact


InstitutionPagedResponse = create_paged_response_class_generic(Institution)


class Institutions(BaseResource):
    def pages(self) -> InstitutionPagedResponse:
        page = self._first_page()
        yield page

        while page.next is not None:
            page = InstitutionPagedResponse.from_dict(
                self.session.get_meta_resource(page.next)
            )
            yield page

    def _first_page(self) -> InstitutionPagedResponse:
        response = self.session.get(
            "/institutions",
            params={"expand": "true", "offset": 0},
            do_auth=False,
            api_type=API.UAC,
        )
        return InstitutionPagedResponse.from_dict(response)

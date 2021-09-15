from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict

from dataclasses_json import Undefined, dataclass_json

from piate.api.resources.base import BaseResource
from piate.api.response import create_paged_response_class_generic
from piate.api.session import Session


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Domain:
    code: str
    name: str
    level: int
    subdomains: List["Domain"] = field(default_factory=list)

    eurovoc_code: Optional[str] = field(default=None)
    cjeu_code: Optional[str] = field(default=None)
    lookups: Optional[List[str]] = field(default_factory=list)

    def compact(self) -> Dict:
        compact = {
            "code": self.code,
            "name": self.name,
            "level": self.level,
            "subdomains": self.subdomains,
        }

        if self.eurovoc_code:
            compact["eurovoc_code"] = self.eurovoc_code

        if self.cjeu_code:
            compact["cjeu_code"] = self.cjeu_code

        if len(self.lookups):
            compact["lookups"] = self.lookups

        return compact


DomainPagedResponse = create_paged_response_class_generic(Domain)


class Domains(BaseResource):
    def list(self) -> DomainPagedResponse:
        response = self.session.get("/domains/_tree", do_auth=False)
        return DomainPagedResponse.from_dict(response)

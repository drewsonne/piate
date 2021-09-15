from dataclasses import dataclass
from typing import Optional, Dict

from dataclasses_json import dataclass_json, Undefined

from piate.api import API
from piate.api.resources.base import BaseResource
from piate.api.response import create_paged_response_class_generic, Meta


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Language:
    meta: Meta
    code: str
    name: str
    is_official: bool

    def compact(self) -> Dict:
        return {"code": self.code, "name": self.name, "is_official": self.is_official}


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class QueryOperators:
    meta: Meta
    code: str
    name: str

    def compact(self) -> Dict:
        return {"code": self.code, "name": self.name}


LanguagePagedResponse = create_paged_response_class_generic(Language)
QueryOperatorsPagedResponse = create_paged_response_class_generic(QueryOperators)


class Inventories(BaseResource):
    def pages_languages(
        self, translation_language: Optional[str] = None
    ) -> LanguagePagedResponse:
        params = {"expand": "true", "offset": 0}
        if translation_language is not None:
            params["trans_lang"] = translation_language
        page = LanguagePagedResponse.from_dict(
            self.session.get(
                "/inventories/_languages",
                params=params,
                do_auth=False,
                api_type=API.EM,
            )
        )
        yield page

        while page.next is not None:
            page = LanguagePagedResponse.from_dict(
                self.session.get_meta_resource(page.next)
            )
            yield page

    def pages_query_operators(
        self, translation_language: Optional[str] = None
    ) -> LanguagePagedResponse:
        params = {"expand": "true", "offset": 0}
        if translation_language is not None:
            params["trans_lang"] = translation_language
        page = LanguagePagedResponse.from_dict(
            self.session.get(
                "/inventories/_query-operators",
                params=params,
                do_auth=False,
                api_type=API.EM,
            )
        )
        yield page

        while page.next is not None:
            page = LanguagePagedResponse.from_dict(
                self.session.get_meta_resource(page.next)
            )
            yield page

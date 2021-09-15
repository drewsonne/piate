from dataclasses import dataclass, field
from typing import Optional, Dict, Type, TypeVar, Generator

from dataclasses_json import dataclass_json, Undefined

from piate.api import API
from piate.api.resources import BaseResource
from piate.api.response import create_paged_response_class_generic, Meta

T = TypeVar("T")


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class InventoryElement:
    meta: Meta
    code: str
    name: str
    is_official: Optional[bool] = field(default=None)
    deprecated: Optional[bool] = field(default=None)

    def compact(self) -> Dict:

        compact = {"code": self.code, "name": self.name}
        if self.is_official is not None:
            compact["is_official"] = self.is_official
        if self.deprecated:
            compact["deprecated"] = self.deprecated

        return compact


InventoryElementsResponse = create_paged_response_class_generic(InventoryElement)


class Inventories(BaseResource):
    def pages_languages(
        self, translation_language: Optional[str] = None
    ) -> InventoryElementsResponse:
        return self._pages(
            InventoryElementsResponse,
            "/inventories/_languages",
            translation_language,
        )

    def pages_query_operators(
        self, translation_language: Optional[str] = None
    ) -> InventoryElementsResponse:
        return self._pages(
            InventoryElementsResponse,
            "/inventories/_query-operators",
            translation_language,
        )

    def pages_term_types(
        self, translation_language: Optional[str] = None
    ) -> Generator[InventoryElementsResponse, None, None]:
        return self._pages(
            InventoryElementsResponse,
            "/inventories/_term-types",
            translation_language,
        )

    def pages_searchable_fields(
        self, translation_language: Optional[str] = None
    ) -> Generator[InventoryElementsResponse, None, None]:
        return self._pages(
            InventoryElementsResponse,
            "/inventories/_searchable-fields",
            translation_language,
        )

    def pages_primarities(
        self, translation_language: Optional[str] = None
    ) -> Generator[InventoryElementsResponse, None, None]:
        return self._pages(
            InventoryElementsResponse, "/inventories/_primarities", translation_language
        )

    def pages_reliabilities(
        self, translation_language: Optional[str] = None
    ) -> Generator[InventoryElementsResponse, None, None]:
        return self._pages(
            InventoryElementsResponse,
            "/inventories/_reliabilities",
            translation_language,
        )

    def _pages(
        self, cls: T, path: str, translation_language: Optional[str] = None
    ) -> Generator[T, None, None]:
        params = {"expand": "true", "offset": 0}
        if translation_language is not None:
            params["trans_lang"] = translation_language
        page = cls.from_dict(
            self.session.get(
                path,
                params=params,
                do_auth=False,
                api_type=API.EM,
            )
        )
        yield page

        while page.next is not None:
            page = cls.from_dict(self.session.get_meta_resource(page.next))
            yield page

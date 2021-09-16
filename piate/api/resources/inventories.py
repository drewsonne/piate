from dataclasses import dataclass, field
from typing import Optional, TypeVar, Generator, List, Callable, TypedDict

from dataclasses_json import dataclass_json, Undefined

from piate.api import API
from piate.api.resources import BaseResource
from piate.api.response import Meta

T = TypeVar("T")


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class InventoryElement:
    meta: Meta
    code: str
    name: str
    is_official: Optional[bool] = field(default=None)
    deprecated: Optional[bool] = field(default=None)

    class Compact(TypedDict):
        code: str
        name: str
        deprecated: Optional[bool]
        is_official: Optional[bool]

    def compact(self) -> Compact:
        compact = {"code": self.code, "name": self.name}
        if self.is_official is not None:
            compact["is_official"] = self.is_official
        if self.deprecated:
            compact["deprecated"] = self.deprecated
        return compact


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class InventoryElementsResponse:
    items: List[InventoryElement]

    meta: Meta

    offset: Optional[int] = field(default=None)
    limit: Optional[int] = field(default=None)
    size: Optional[int] = field(default=None)

    next: Optional[Meta] = field(default=None)

    def compact(self) -> List[InventoryElement.Compact]:
        return [item.compact() for item in self.items]


def pages_inventory_method(
    path: str,
) -> Callable[
    ["Inventories", Optional[str]], Generator[InventoryElementsResponse, None, None]
]:
    return lambda self, translation_language=None: self._pages(
        f"/inventories/_{path}", translation_language
    )


def get_inventory_method(
    path: str,
) -> Callable[
    ["Inventories", Optional[str], Optional[str], Optional[bool]], InventoryElement
]:
    def inventory_method(
        self: "Inventories",
        code: Optional[str],
        name: Optional[str],
        is_official: Optional[bool],
    ) -> InventoryElement:

        official_func = lambda l: (is_official is None) or (
            l.is_official == is_official
        )

        filter_by_name = lambda l: (l.name == name) and official_func(l)
        filter_by_code = lambda l: (l.code == code) and official_func(l)
        filter_func = filter_by_name if code is None else filter_by_code

        response = {}
        for page in self._pages(f"/inventories/_{path}"):
            for language in page.items:
                if filter_func(language):
                    response = language
        return response

    return inventory_method


class Inventories(BaseResource):
    get_language = get_inventory_method("languages")
    pages_languages = pages_inventory_method("languages")

    get_term_type = get_inventory_method("term-types")
    pages_term_types = pages_inventory_method("term-types")

    get_primarity = get_inventory_method("primarities")
    pages_primarities = pages_inventory_method("primarities")

    get_reliability = get_inventory_method("reliabilities")
    pages_reliabilities = pages_inventory_method("reliabilities")

    get_query_operator = get_inventory_method("query-operators")
    pages_query_operators = pages_inventory_method("query-operators")

    get_searchable_field = get_inventory_method("searchable-fields")
    pages_searchable_fields = pages_inventory_method("searchable-fields")

    def _pages(
        self, path: str, translation_language: Optional[str] = None
    ) -> Generator[InventoryElementsResponse, None, None]:
        params = {"expand": "true", "offset": 0}
        if translation_language is not None:
            params["trans_lang"] = translation_language
        page = InventoryElementsResponse.from_dict(
            self.session.get(
                path,
                params=params,
                do_auth=False,
                api_type=API.EM,
            )
        )
        yield page

        while page.next is not None:
            page = InventoryElementsResponse.from_dict(
                self.session.get_meta_resource(page.next)
            )
            yield page

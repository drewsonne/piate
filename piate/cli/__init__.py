from dataclasses import dataclass
from typing import Optional

import cloup
from cloup.constraints import RequireExactly

from piate.api.client import Client
from piate.api.credentials import Credentials
from piate.api.session import Session
from piate.cli.format import Format
from piate.cli.render import pages_response_iterator, page_response


@dataclass
class ContextObj:
    client: Client
    format: Format


@cloup.group()
@cloup.option(
    "--username",
    "-U",
    metavar="USERNAME",
    help="Username to request against the API",
    required=False,
)
@cloup.option(
    "--api-key",
    "-K",
    metavar="API_KEY",
    help="API Key to use to request against the API",
    required=False,
)
@cloup.option("--format", default="json", type=cloup.Choice(["json", "json-lines"]))
@cloup.pass_context
def run(ctx: cloup.Context, username: str, api_key: str, format: str):
    ctx.obj = ContextObj(
        client=Client(Session(Credentials(username=username, api_key=api_key))),
        format=Format(format),
    )


"""
Inventories
"""


@run.group()
def inventories():
    ...


@inventories.command("list-languages")
@cloup.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@cloup.pass_obj
def inventories_languages(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_languages(**kwargs), obj.format
    )


@inventories.command("get-language", help="Fetch a language")
@cloup.option(
    "--official/--non-official",
    default=None,
    help="Only return if the result is an official language.",
)
@cloup.option_group(
    "Search Options",
    cloup.option("--code", metavar="CODE", help="Fetch a language by code"),
    cloup.option("--name", metavar="NAME", help="Fetch a language by name"),
    constraint=RequireExactly(1),
)
@cloup.pass_obj
def inventories_language(
    obj: ContextObj,
    code: Optional[str] = None,
    name: Optional[str] = None,
    official: Optional[bool] = None,
):
    official_func = lambda l: (official is None) or (l.is_official == official)

    filter_by_name = lambda l: (l.name == name) and official_func(l)
    filter_by_code = lambda l: (l.code == code) and official_func(l)
    filter_func = filter_by_name if code is None else filter_by_code

    response = {}
    for page in obj.client.inventories.pages_languages():
        for language in page.items:
            if filter_func(language):
                response = language

    page_response(response, obj.format)


@inventories.command("list-query-operators")
@cloup.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@cloup.pass_obj
def inventories_query_operators(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_query_operators(**kwargs), obj.format
    )


@inventories.command("list-term-types")
@cloup.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@cloup.pass_obj
def inventories_term_types(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_term_types(**kwargs), obj.format
    )


@inventories.command("list-searchable-fields")
@cloup.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@cloup.pass_obj
def inventories_searchable_fields(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_searchable_fields(**kwargs), obj.format
    )


@inventories.command("list-primarities")
@cloup.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@cloup.pass_obj
def inventories_primarities(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_primarities(**kwargs), obj.format
    )


@inventories.command("list-reliabilities")
@cloup.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@cloup.pass_obj
def inventories_reliabilities(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_reliabilities(**kwargs), obj.format
    )


""""
Domains
"""


@run.command("list-domains")
@cloup.pass_obj
def domains(obj: ContextObj):
    page_response(obj.client.domains.list(), obj.format)


"""
Collections
"""


@run.command("list-collections")
@cloup.pass_obj
def collections(obj: ContextObj):
    pages_response_iterator(obj.client.collections.pages(), obj.format)


"""
Institutions
"""


@run.command("list-institutions")
@cloup.pass_obj
def institutions(obj: ContextObj):
    pages_response_iterator(obj.client.institutions.pages(), obj.format)


"""
Entries
"""


@run.group("entries")
def entries():
    ...


@entries.command("search-entries")
def entries_search():
    raise NotImplementedError()


@entries.command("multi-search-entries")
def entries_multi_search():
    raise NotImplementedError()


if __name__ == "__main__":
    run()

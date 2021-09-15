from dataclasses import dataclass

import click

import piate
from piate.api.client import Client
from piate.api.credentials import Credentials
from piate.api.session import Session
from piate.cli.format import Format
from piate.cli.render import pages_response_iterator, page_response


@dataclass
class ContextObj:
    client: Client
    format: Format


@click.group()
@click.option(
    "--username",
    "-U",
    metavar="USERNAME",
    help="Username to request against the API",
    required=False,
)
@click.option(
    "--api-key",
    "-K",
    metavar="API_KEY",
    help="API Key to use to request against the API",
    required=False,
)
@click.option("--format", default="json", type=click.Choice(["json", "json-lines"]))
@click.pass_context
def run(ctx: click.Context, username: str, api_key: str, format: str):
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
@click.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@click.pass_obj
def inventories_languages(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_languages(**kwargs), obj.format
    )


@inventories.command("list-query-operators")
@click.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@click.pass_obj
def inventories_query_operators(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_query_operators(**kwargs), obj.format
    )


@inventories.command("list-term-types")
@click.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@click.pass_obj
def inventories_term_types(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_term_types(**kwargs), obj.format
    )


@inventories.command("list-searchable-fields")
@click.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@click.pass_obj
def inventories_searchable_fields(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_searchable_fields(**kwargs), obj.format
    )


@inventories.command("list-primarities")
@click.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@click.pass_obj
def inventories_primarities(obj: ContextObj, translation_language: str):
    kwargs = {}
    if translation_language is not None:
        kwargs["translation_language"] = translation_language
    pages_response_iterator(
        obj.client.inventories.pages_primarities(**kwargs), obj.format
    )


@inventories.command("list-reliabilities")
@click.option(
    "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
)
@click.pass_obj
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
@click.pass_obj
def domains(obj: ContextObj):
    page_response(obj.client.domains.list(), obj.format)


"""
Collections
"""


@run.command("list-collections")
@click.pass_obj
def collections(obj: ContextObj):
    pages_response_iterator(obj.client.collections.pages(), obj.format)


"""
Institutions
"""


@run.command("list-institutions")
@click.pass_obj
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

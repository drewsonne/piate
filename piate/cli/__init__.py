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
def inventories_languages():
    piate.client()
    raise NotImplementedError()


@inventories.command("list-query-operators")
def inventories_query_operators():
    raise NotImplementedError()


@inventories.command("list-term-types")
def inventories_term_types():
    raise NotImplementedError()


@inventories.command("list-searchable-fields")
def inventories_searchable_fields():
    raise NotImplementedError()


@inventories.command("list-primarities")
def inventories_primarities():
    raise NotImplementedError()


@inventories.command("list-reliabilities")
def inventories_reliabilities():
    raise NotImplementedError()


""""
Domains
"""


@run.command("list-domains")
@click.pass_obj
def domains(obj: ContextObj):
    page_response(obj.client.domains.list(), obj.format)


@run.command("list-collections")
@click.pass_obj
def collections(obj: ContextObj):
    pages_response_iterator(obj.client.collections.pages(), obj.format)


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

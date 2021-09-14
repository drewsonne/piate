from dataclasses import dataclass

import click

import piate
from piate.api.client import Client
from piate.api.credentials import Credentials
from piate.api.session import Session
from piate.cli.render import response


@dataclass
class ContextObj:
    client: Client


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
@click.pass_context
def run(ctx: click.Context, username: str, api_key: str):
    ctx.obj = ContextObj(
        client=Client(Session(Credentials(username=username, api_key=api_key)))
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
def domains():
    raise NotImplementedError()


@run.command("list-collections")
@click.pass_obj
def collections(obj: ContextObj):
    response(obj.client.collections.list())


@run.command("list-institutions")
def institutions():
    raise NotImplementedError()


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

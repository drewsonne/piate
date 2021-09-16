import cloup

from piate.api.client import Client
from piate.api.credentials import Credentials
from piate.api.session import Session
from piate.cli.context import ContextObj
from piate.cli.format import Format
from piate.cli.inventories import (
    generate_inventory_get_command,
    generate_inventory_list_command,
)
from piate.cli.render import pages_response_iterator, page_response


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


generate_inventory_get_command(inventories, "language", has_official=True)
generate_inventory_list_command(inventories, "languages")

generate_inventory_get_command(inventories, "primarity")
generate_inventory_list_command(inventories, "primarities")

generate_inventory_get_command(inventories, "query-operator")
generate_inventory_list_command(inventories, "query-operators")

generate_inventory_get_command(inventories, "reliability")
generate_inventory_list_command(inventories, "reliabilities")

generate_inventory_get_command(inventories, "searchable-field")
generate_inventory_list_command(inventories, "searchable-fields")

generate_inventory_get_command(inventories, "term-type")
generate_inventory_list_command(inventories, "term-types")


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

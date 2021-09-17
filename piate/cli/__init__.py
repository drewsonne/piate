import cloup

from piate.api.client import Client
from piate.api.credentials import Credentials
from piate.api.session import Session
from piate.cli.context import ContextObj
from piate.cli.format import Format
from piate.cli.resources.inventories import (
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


@entries.command(
    "search-entries",
    epilog="""
\b
See https://documenter.getpostman.com/view/4028985/RztoMTwn#72dd2d11-d83c-4cbd-b5d9-2d9ee97cf379
for more details regarding the search options.""",
)
@cloup.option(
    "--query",
    "-q",
    metavar="QUERY",
    help="The string to parse/analyse/search",
    required=False,
)
@cloup.option(
    "--source",
    "-s",
    metavar="SOURCE",
    help=" The source language of the terminology data",
)
@cloup.option(
    "--target",
    "-t",
    metavar="TARGET",
    help="The target languages of the terminology data",
    multiple=True,
)
@cloup.option(
    "--search-in-fields",
    "-sF",
    metavar="FIELDS",
    help="The fields in which the search will be performed",
    multiple=True,
)
@cloup.option(
    "--search-in-term-types",
    "-sT",
    metavar="TERM_TYPE",
    type=int,
    help="The term-entry codes in which the search will be performed",
    multiple=True,
)
@cloup.option(
    "--query-operator",
    "-Q",
    type=int,
    metavar="OPERATOR_CODE",
    help="The operator code of the query",
    required=False,
)
@cloup.option(
    "--domain-cascade/--no-domain-cascade",
    "-c",
    help="To apply or not the domain cascading while filtering by domains",
    required=False,
)
@cloup.option("--filter", "-F", help="Provide a filter")
@cloup.pass_obj
def entries_search(
    obj: ContextObj, query: str, source: str, targets: str, search_in_fields
):
    """
    Search the IATE database for entries

    \033[1mFilters\033[0m

    \b
    When using the \033[3m--filter\033[0m option, the arguments are parsed based on the structure:
    \b
        Name=\033[3m<name>\033[0m:Values=\033[3m<value_list>\033[0m[;Name=\033[3m<name>\033[0m:Values=\033[3m<value_list>\033[0m]

    Multiple filter statements can be concatenated with a ';'.

    \b
    \033[3m<name>\033[0m
    Which type of filter this entry will target.
    Currently supports:
      - domains
      - entry_collection
      - entry_institution_owner
      - entry_primarity
      - source_term_reliability
      - target_term_reliability

    \b
    \033[3m<value_list>\033[0m
    Comma separated list of codes.
    Example: 5,2,4 is an array of values [5, 2, 4].


    """
    raise NotImplementedError()


@entries.command("multi-search-entries")
def entries_multi_search():
    raise NotImplementedError()


if __name__ == "__main__":
    run()

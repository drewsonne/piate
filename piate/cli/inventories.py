from typing import Optional

import click
import cloup
from cloup.constraints import RequireExactly

from piate.cli.context import ContextObj
from piate.cli.render import page_response, pages_response_iterator


def generate_inventory_get_command(
    inventories: click.Group, entity: str, has_official: Optional[bool] = False
):
    """
    Generate a CLI command for retrieving a list of entities from inventory
    """

    command_decorator = inventories.command(f"get-{entity}", help=f"Fetch a {entity}")
    has_official_decorator = cloup.option(
        "--official/--non-official",
        default=None,
        help=f"Only return if the result is an official {entity}.",
    )

    @cloup.option_group(
        "Search Options",
        cloup.option(
            "--code", metavar="CODE", help=f"Fetch a {entity} by code", type=int
        ),
        cloup.option("--name", metavar="NAME", help=f"Fetch a {entity} by name"),
        constraint=RequireExactly(1),
    )
    @cloup.pass_obj
    def inventory_entity(
        obj: ContextObj,
        code: Optional[str] = None,
        name: Optional[str] = None,
        official: Optional[bool] = None,
    ):
        entity_fetcher = getattr(
            obj.client.inventories, f"get_{entity.replace('-', '_')}"
        )
        page_response(entity_fetcher(code, name, official), obj.format)

    if has_official:
        inventory_entity = has_official_decorator(inventory_entity)

    inventory_entity = command_decorator(inventory_entity)
    return inventory_entity


def generate_inventory_list_command(inventories: click.Group, entities: str):
    """
    Generate a CLI command for retrieving an entity from inventories
    """

    @inventories.command(f"list-{entities}", help=f"Fetch a list of {entities}")
    @cloup.option(
        "--translation-language", "-L", metavar="TRANSLATION_LANGUAGE", required=False
    )
    @cloup.pass_obj
    def inventory_entities(obj: ContextObj, translation_language: str):
        kwargs = {}
        if translation_language is not None:
            kwargs["translation_language"] = translation_language
        entity_fetcher = getattr(
            obj.client.inventories, f"pages_{entities.replace('-', '_')}"
        )
        pages_response_iterator(entity_fetcher(**kwargs), obj.format)

    return inventory_entities

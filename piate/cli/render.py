import dataclasses
import json
from functools import reduce
from json import JSONEncoder
from typing import Any, List, Iterator

import click

from piate.cli.format import Format


class _IATEResponseEncoder(JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            if hasattr(o, "items"):
                return [i.compact() for i in o.items]
            elif hasattr(o, "compact"):
                return o.compact()
            else:
                return dataclasses.asdict(o)
        else:
            return super().default(o)


def response(obj: Any):
    click.echo(json.dumps(obj, cls=_IATEResponseEncoder, indent=4))


def response_lines(obj: List[Any]):
    for item in obj:
        click.echo(json.dumps(item, cls=_IATEResponseEncoder))


def pages_response_iterator(paginator: Iterator, format: Format):
    if format == Format.JSON:
        response(list(reduce(lambda items, page: items + page.items, paginator, [])))
    elif format == Format.JSON_LINES:
        for page in paginator:
            response_lines(page.items)
    else:
        raise RuntimeError(f"Unexpected output format: {format=}")


def page_response(page, format: Format):
    if format == Format.JSON:
        response(page)
    elif format == Format.JSON_LINES:
        response_lines(page.items)
    else:
        raise RuntimeError(f"Unexpected output format: {format=}")

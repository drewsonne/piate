import dataclasses
import json
from json import JSONEncoder
from typing import Any, List

import click


class _IATEResponseEncoder(JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            if hasattr(o, "items"):
                return [i.compact() for i in o.items]
            else:
                return o.to_dict()
        else:
            return super().default(o)


def response(obj: Any):
    click.echo(json.dumps(obj, cls=_IATEResponseEncoder, indent=4))


def response_lines(obj: List[Any]):
    for item in obj:
        click.echo(json.dumps(item, cls=_IATEResponseEncoder))

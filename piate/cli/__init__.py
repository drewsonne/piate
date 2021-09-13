import click


@click.group()
def run():
    ...


## INVENTORIES


@run.group()
def inventories():
    ...


@inventories.command("list-languages")
def inventories_languages():
    raise NotImplemented()


@inventories.command("list-query-operators")
def inventories_query_operators():
    raise NotImplemented()


@inventories.command("list-term-types")
def inventories_term_types():
    raise NotImplemented()


@inventories.command("list-searchable-fields")
def inventories_searchable_fields():
    raise NotImplemented()


@inventories.command("list-primarities")
def inventories_primarities():
    raise NotImplemented()


@inventories.command("list-reliabilities")
def inventories_reliabilities():
    raise NotImplemented()


## DOMAINS

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


## DOMAINS


@run.command("list-domains")
def domains():
    raise NotImplementedError()


@run.command("list-collections")
def collections():
    raise NotImplementedError()


@run.command("list-institutions")
def institutions():
    raise NotImplementedError()


## Entries


@run.group("entries")
def entries():
    ...


@entries.command("search-entries")
def entries_search():
    raise NotImplementedError()


@entries.command("multi-search-entries")
def entries_multi_search():
    raise NotImplementedError()

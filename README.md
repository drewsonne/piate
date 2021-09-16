# piate

A python library and cli tool to interact with the [IATE (**I**nter**a**ctive **T**erminology for **E**urope)](https://iate.europa.eu/home) database. 

 - [CLI tool](#cli-tool)
 - [Library](#api)

# Installing

```commandline
pip install piate
```

# <a name="cli-tool"></a>CLI tool

```shell
$ iate --help
```


## Filtering

It's suggested to use the  [`jq`](https://stedolan.github.io/jq/) to filter the responses on the command line.

For example, only select official languages:
```shell
iate inventories list-languages | jq '[.[] | select(.is_official == true)] | length'
```

# <a name="api"></a>Library

 - [client()](#client)
   - [collections](#collections)
     - [pages()](#collection-pages)
   - [institutions](#institutions)
     - [pages()](#institution-pages)
   - [domains](#domains)
     - [list()](#domains-list)
   - [inventories](#inventories)
     - [pages_languages()](#inventories-pages_languages)
     - [pages_query_operators()](#inventories-pages_query_operators)
     - [pages_term_types()](#inventories-pages_term_types)
     - [pages_searchable_fields()](#inventories-pages_searchable_fields)
     - [pages_primarities()](#inventories-pages_primarities)
     - [pages_reliabilities()](#inventories-pages_reliabilities)

## <a name="client">client(**kwargs)</a>

The entrypoint into the library, allowing the provision of authentication.

#### Parameters

 - **username** _(string)_ -- Username to use to authenticate against the API. Conflicts with `session`. Requires `password`.
 - **password** _(string)_ -- Password to use to authenticate against the API. Conflicts with `session`. Requires `username`.
 - **session** _(piate.api.session.Session)_ -- Session object to use to authenticate against the API. Conflicts with `username` and `password`.

#### Examples

```python
# Example with username and password
import piate

iate_client = piate.client(username="myusername", api_key="...")
```

```python
# Example with session object
import piate
from piate.api.session import Session
from piate.api.credentials import Credentials

iate_client = piate.client(
    session=Session(
        credentials=Credentials(
            username="myusername", 
            api_key="..."
        )
    )
)
```

## <a name="collections"></a>Collections

A resource representing collections

```python
import piate

collections = piate.client(...).collections
```

These are the available methods:

 - [_`pages()`_](#collection-pages)

### <a name="collection-pages">**pages()**</a>

Iterate through pages of responses for Collections objects.

#### Examples

```python
for page in collections.pages():
    for collection in page.items:
        print(collection.name)
```

## <a name="institutions"></a>Institutions

A resource representing institutions

```python
import piate 

institutions = piate.client(...).institutions
```

These are the available methods:

 - [_`pages()`_](#institution-pages)

### <a name="institution-pages">**pages()**</a>

Iterate through pages of response for Institutions objects.

#### Examples 

```python
for page in institutions.pages():
    for institution in page.items:
        print(institution.name)
```

## <a name="domains"></a>Domains

A resource representing domains

```python
import piate

domains = piate.client(...).domains
```

These are the available methods: 

 - [_`list()`_](#domains-list)

### <a name="domains-list">**list()**</a>

List all the available domains.

#### Examples

```python
for domain in domains.list():
    print(domain.name)
```

## <a name=""></a>Inventories

A resoure representing inventories

```python
import piate

inventories = piate.client(...).inventories
```

These are the available methods:

 - [_`pages_languages()`_](#inventories-pages_languages)
 - [_`pages_query_operators()`_](#inventories-pages_query_operators)
 - [_`pages_term_types()`_](#inventories-pages_term_types)
 - [_`pages_searchable_fields()`_](#inventories-pages_searchable_fields)
 - [_`pages_primarities()`_](#inventories-pages_primarities)
 - [_`pages_reliabilities()`_](#inventories-pages_reliabilities)

### <a name="inventories-pages_languages">**pages_languages(\*\*kwargs)**</a>

Iterate through pages of response for language objects.

#### Parameters

 - **translation_language** _(string)_ -- Translation Language

#### Examples

```python
for page in inventories.pages_languages(translation_language="en"):
    for language in page.items:
        print(language.name)
```

### <a name="inventories-pages_query_operators">**pages_query_operators(\*\*kwargs)**</a>

Iterate through pages of response for language objects.

#### Parameters

 - **translation_language** _(string)_ -- Translation Language

#### Examples

```python
for page in inventories.pages_query_operators(translation_language="en"):
    for query_operators in page.items:
        print(query_operators.name)
```

### <a name="inventories-pages_term_types">**pages_term_types(\*\*kwargs)**</a>

Iterate through pages of response for language objects.

#### Parameters

 - **translation_language** _(string)_ -- Translation Language

#### Examples

```python
for page in inventories.pages_term_types(translation_language="en"):
    for term_types in page.items:
        print(term_types.name)
```

### <a name="inventories-pages_searchable_fields">**pages_searchable_fields(\*\*kwargs)**</a>

Iterate through pages of response for language objects.

#### Parameters

 - **translation_language** _(string)_ -- Translation Language

#### Examples

```python
for page in inventories.pages_searchable_fields(translation_language="en"):
    for searchable_field in page.items:
        print(searchable_field.name)
```

### <a name="inventories-pages_primarities">**pages_primarities(\*\*kwargs)**</a>

Iterate through pages of response for language objects.

#### Parameters

 - **translation_language** _(string)_ -- Translation Language

#### Examples

```python
for page in inventories.pages_primarities(translation_language="en"):
    for primarities in page.items:
        print(primarities.name)
```

### <a name="inventories-pages_reliabilities">**pages_reliabilities(\*\*kwargs)**</a>

Iterate through pages of response for language objects.

#### Parameters

 - **translation_language** _(string)_ -- Translation Language

#### Examples

```python
for page in inventories.pages_reliabilities(translation_language="en"):
    for reliabilities in page.items:
        print(reliabilities.name)
```

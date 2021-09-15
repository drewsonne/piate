# piate

A python library and cli tool to interact with the [IATE (**I**nter**a**ctive **T**erminology for **E**urope)](https://iate.europa.eu/home) database. 

 - [CLI tool](#cli-tool)
 - [Library](#api)

# Installing

```commandline
pip install piate
```

# <a name="cli-tool"></a>CLI tool

Currently working commands:

 - `iate list-collections`
 - `iate list-domains`
 - `iate list-institutions`
 - `iate inventories list-languages`
 - `iate inventories list-primarities`
 - `iate inventories list-query-operators`
 - `iate inventories list-reliabilities`
 - `iate inventories list-searchable-fields`
 - `iate inventories list-term-types`

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

A resource represneting institutions

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

## 
# piate

A python library and cli tool to interact with the [IATE (**I**nter**a**ctive **T**erminology for **E**urope)](https://iate.europa.eu/home) database. 

# Installing

```commandline
pip install piate
```

# Library

## client(...)

The entrypoint into the library, allowing the provision of authentication.

### With username and password

```python
import piate

iate = piate.client(username="myusername", api_key="...")
```

### With prebuilt session

```python
import piate
from piate.api.session import Session
from piate.api.credentials import Credentials

iate = piate.client(
    session=Session(
        credentials=Credentials(
            username="myusername", 
            api_key="..."
        )
    )
)
```

## Collections

```python
import piate

for page in piate.client(...).collections.pages():
    for collection in page.items:
        print(collection.name)
```

### 

## CLI tool

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

### Filtering

It's suggested to use the  [`jq`](https://stedolan.github.io/jq/) to filter the responses on the command line.

For example, only select official languages:
```shell
iate inventories list-languages | jq '[.[] | select(.is_official == true)] | length'
```
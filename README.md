# piate

A python library and cli tool to interact with the [IATE (**I**nter**a**ctive **T**erminology for **E**urope)](https://iate.europa.eu/home) database. 

# Installing

```commandline
pip install piate
```

## CLI tool

Currently working commands:

 - `iate list-collections`
 - `iate list-domains`
 - `iate list-institutions`

### Filtering

It's suggested to use the  [`jq`](https://stedolan.github.io/jq/) to filter the responses on the command line.

For example, only select official languages:
```shell
iate inventories list-languages | jq '[.[] | select(.is_official == true)] | length'
```
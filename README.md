# README

## Overview

A custom Jinja filter for Sceptre for unquoting resolvers appearing in
var files.

## Motivation

In Sceptre, resolvers are an essential feature for simplifying complex
configurations by enabling dynamic data retrieval. Resolvers such as
`!stack_output_external` and `!stack_output` are particularly useful
for referencing output values from other stacks or external sources,
among many others.

When using resolvers in var files, however, they must be protected from
being interpreted as YAML tags by the YAML loader.

This plugin addresses this challenge by allowing you to safely include
resolvers in your var files. It ensures that resolvers are not processed
as YAML tags by the loader, and then turned back into YAML tags after
Jinja interpolation in the generated config.

## Installation

Installation instructions

To install directly from PyPI
```shell
pip install jinja-unquote-resolvers-filter
```

To install from the git repo
```shell
pip install git+https://github.com/Sceptre/jinja-unquote-resolvers-filter.git
```

## Usage/Examples

In your var file:

```yaml
Subnets:
  - '!stack_output_external mystack::subnet_a'  # Quotes needed to protect a YAML tag.
  - '!stack_output_external mystack::subnet_b'

VPC: '!stack_output_external mystack::vpc_id'
```

In your config:

```yaml
j2_environment:
  extensions:
    - jinja_unquote_resolvers_filter.UnquoteResolversFilterExtension

sceptre_user_data:
  subnets:
    {{ var.Subnets | unquote_resolvers(output_indent=4, trim=True) }}
  vpc: {{ var.VPC }}  # This filter is not needed if the quoted resolvers are passed in as scalars.
```

## Arguments

- `indent` (optional, default=2): The number of spaces to use for indentation of nested structures in the output YAML.
- `output_indent` (optional, default=0): The number of spaces to use for indentation of the entire output YAML.
- `trim` (optional, default=False): Whether to trim leading and trailing spaces in the output YAML.

## Limitations

At this time, resolver expressions must be wrapped in a single line of text. That is, instead of:

```yaml
my_multiline_resolver: |
  !from_json
    - !request http://www.whatever.com
```

Instead write:

```yaml
my_multiline_resolver: '!from_json [!request http://www.whatever.com]'
```

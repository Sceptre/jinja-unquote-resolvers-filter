# README

## Overview

A brief description. Be clear about the purpose of the resolver,
its capabilities and limitations.

## Installation

Installation instructions

To install directly from PyPI
```shell
pip install sceptre-resolver-template
```

To install from the git repo
```shell
pip install git+https://github.com/Sceptre/sceptre-resolver-template.git
```

## Usage/Examples

Refer to the [Sceptre resolver docs](https://docs.sceptre-project.org/latest/docs/resolvers.html#resolvers)
for more information.

```yaml
parameter|sceptre_user_data:
  <name>: !custom <args>
```

## Example

```yaml
parameters:
  message: !custom "HelloWorld"
```

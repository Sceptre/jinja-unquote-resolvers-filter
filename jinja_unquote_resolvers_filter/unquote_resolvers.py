from typing import Any, Dict, List, Union

import yaml
from yaml.nodes import ScalarNode

from functools import singledispatch
from textwrap import indent as textwrap_indent

try:
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeDumper  # type: ignore


class CustomDumper(SafeDumper):
    pass


def unquoted_tag_representer(dumper: CustomDumper, data: "Tag") -> ScalarNode:
    return dumper.represent_scalar(data.tag, data.value, style="")


class Tag:
    def __init__(self, tag: str, value: str) -> None:
        self.tag = tag
        self.value = value


CustomDumper.add_representer(Tag, unquoted_tag_representer)


def unquote_resolvers(
    data: Union[Dict, List],
    indent: int = 2,
    output_indent: int = 0,
    trim: bool = False,
    *args: Any,
    **kw: Any
) -> str:
    """
    Remove quotes around resolver expressions and
    produce nice YAML.

    :param data: The input data as a dictionary or list
      containing resolver expressions.
    :param indent: The number of spaces to use for indentation
      of nested structures in the output YAML.  Default is 2
      spaces.
    :param output_indent: The number of spaces to use for
      indentation of the entire output YAML. Default is 0
      (no indentation).

    :returns: A formatted YAML string with unquoted resolver
      expressions and the specified indentation settings.
    """

    @singledispatch
    def process_item(item: Any) -> Any:
        return item

    @process_item.register(str)
    def _(item: str) -> Any:
        if item.startswith("!"):
            if "\n" in item:
                raise NotImplementedError("Multiline expressions not supported")
            tag_name, tag_body = item.split(" ", 1)
            return Tag(tag_name, tag_body)
        return item

    @process_item.register(dict)
    def _(item: Dict) -> Dict:
        return {key: process_item(value) for key, value in item.items()}

    @process_item.register(list)
    def _(item: List) -> List:
        return [process_item(value) for value in item]

    if not isinstance(data, (dict, list)):
        raise TypeError(
            "unquote_resolvers - Input data must be a dict or a list, but got %s"
            % type(data).__name__
        )

    processed_data = process_item(data)

    try:
        transformed = yaml.dump(
            processed_data,
            Dumper=CustomDumper,
            indent=indent,
            allow_unicode=True,
            default_flow_style=False,
            **kw
        )

    except Exception as e:
        raise Exception("unquote_resolvers - %s" % str(e))

    if output_indent > 0:
        transformed = textwrap_indent(transformed, " " * output_indent)

    if trim:
        transformed = transformed.strip()

    return transformed

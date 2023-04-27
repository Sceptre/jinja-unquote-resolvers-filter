from jinja2.ext import Extension
from .unquote_resolvers import unquote_resolvers


class UnquoteResolversFilterExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["unquote_resolvers"] = self.unquote_resolvers_filter

    def unquote_resolvers_filter(self, data, indent=2, output_indent=0, trim=False):
        return unquote_resolvers(
            data, indent=indent, output_indent=output_indent, trim=trim
        )

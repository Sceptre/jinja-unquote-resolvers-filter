from jinja2.ext import Extension
from .unquote_resolvers import unquote_resolvers


class FilterModule:
    def filters(self):
        return {"unquote_resolvers": unquote_resolvers}


class UnquoteResolversFilterExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["unquote_resolvers"] = \
            self.unquote_resolvers_filter

    def unquote_resolvers_filter(self, data, indent=2, output_indent=2):
        return unquote_resolvers(data, indent=indent)

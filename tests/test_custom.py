# -*- coding: utf-8 -*-

from resolver.custom import Custom


class TestCustom:
    resolver = Custom()

    def setup(self):
        self.resolver.argument = "test"

    def test_custom(self):
        self.resolver.resolve()

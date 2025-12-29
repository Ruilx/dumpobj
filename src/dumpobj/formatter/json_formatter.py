# -*- coding: utf-8 -*-
from typing import Any

try:
    import ujson as json
except ImportError:
    import json

from .base_formatter import Formatter
from ..node import Node, ErrorNode

class JSONFormatter(Formatter):
    def __init__(self):
        self.compact = False
        self.indent = 4
        self.ensure_ascii = False

    def _format_key(self, node: Node) -> str:
        return node.get_key()

    def _format_props(self, node: Node) -> tuple[str, str]:
        return node.get_prop("title"), node.get_prop("type")

    def _format_attrs(self, node: Node) -> dict[str, Any]:
        return node.get_attrs()

    def _format_value(self, node: Node) -> str:
        return node.get_value()

    def _format_header(self, key: str, props: tuple[str, str], attrs: dict[str, Any], value: str, indent: int, context: dict[str, Any]):
        return {
            "name": props[0],
            "type": props[1],
            "attrs": attrs,
            "value": value,
        }

    def _format_error(self, key: str, props: tuple[str, str], attrs: dict[str, Any], value: str, indent: int, context: dict[str, Any]):
        return {
            "name": props[0],
            "type": props[1],
            "attrs": attrs,
        }

    def _format_node(self, node: Node, indent: int, context: dict[str, Any]):
        self._pre_node(node, context=context)
        context[]

"""Tests for config.base"""

from typing import Any
from dataclasses import dataclass

import pytest

import deepr as dpr


@dataclass
class A:
    x: Any


class B:
    def __init__(self, *args):
        self.args = args

    def __eq__(self, other):
        return type(self) is type(other) and self.args == other.args


@pytest.mark.parametrize(
    "config, macros, expected",
    [
        (None, None, None),
        ({"type": "test_config_base.A", "x": "$macro:x"}, {"macro": {"x": 1}}, {"type": "test_config_base.A", "x": 1}),
        (
            {"type": "test_config_base.A", "x": "@self"},
            None,
            {"type": "test_config_base.A", "x": {"type": "test_config_base.A", "eval": "skip", "x": "@self"}},
        ),
    ],
)
def test_config_parse_config(config, macros, expected):
    assert dpr.parse_config(config, macros) == expected


@pytest.mark.parametrize(
    "item, expected",
    [
        (None, None),
        (1, 1),
        (3.14, 3.14),
        (True, True),
        (False, False),
        ("hello", "hello"),
        ((1, 2), (1, 2)),
        ([1, 2], [1, 2]),
        ({1: 2}, {1: 2}),
        ({"type": "test_config_base.A", "x": 1}, A(1)),
        ({"type": "test_config_base.B", "*": (1, 2)}, B(1, 2)),
        ({"type": "test_config_base.A", "eval": "skip", "x": 1}, {"type": "test_config_base.A", "x": 1}),
    ],
)
def test_config_from_config(item, expected):
    assert dpr.from_config(item) == expected

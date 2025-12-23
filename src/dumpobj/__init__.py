# -*- coding: utf-8 -*-

"""dumpobj

"""

from typing import TYPE_CHECKING

try:
    from importlib.metadata import version, PackageNotFoundError

    try:
        __version__ = version("dumpobj")
    except PackageNotFoundError:
        __version__ = "0.0.0"
except BaseException:
    __version__ = "0.0.0"

__author__ = "Ruilx"
__email__ = "RuilxAlxa@qq.com"
__license__ = "MIT"
__url__ = "https://github.com/Ruilx/dumpobj"
__description__ = "A utility class for dumping Python objects into a structured format."

if TYPE_CHECKING:
    from ._dumpobj import dump, Dump

def __getattr__(name: str):
    if name in {"dump", "Dump"}:
        from ._dumpobj import dump, Dump
        return {
            "dump": dump,
            "Dump": Dump,
        }[name]
    raise AttributeError(f"module 'dumpobj' has no attribute {name!r}")

def __dir__():
    return sorted(
        list(globals().keys())
        + [
            "dump",
            "Dump",
        ]
    )


__all__ = [
    "dump",
    "Dump",
]

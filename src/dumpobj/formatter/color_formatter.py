# -*- coding: utf-8 -*-
from plain_formatter import PlainFormatter

from colortty import colortty, color, background_color

class ColorFormatter(PlainFormatter):
    Colors = {
        "prop": colortty().set(color.magenta(lighter=True)),
        "prop_title": colortty().set(color.red()),
        "prop_type": colortty().set(color.blue()),
        "prop_ref": colortty().set(color.black(lighter=True)),
        "prop_attr_key": colortty().set(color.yellow()),
        "prop_attr_value": colortty().set(color.green()),
        "prop_value": None,
    }


    def __init__(self):
        ...

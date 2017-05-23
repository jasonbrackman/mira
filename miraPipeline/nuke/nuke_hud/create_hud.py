# -*- coding: utf-8 -*-
import nuke
from get_hud import get_format_hud


def create_hud():
    select_node = nuke.selectedNode()
    text_node = nuke.createNode("Text2", "name %s" % "HUD")
    expression = "[python get_hud(nuke.thisNode())]"
    text_node["message"].setValue(expression)
    text_node["global_font_scale"].setValue(0.7)
    # set pos
    width, height = get_format_hud(text_node).split("*")
    width = int(width)
    height = int(height)
    text_node["box"].setValue([width-700, height-100, width, height-30])
    # set color
    text_node["color"].setValue([1, 0, 0, 1])

# -*- coding: utf-8 -*-
import sys
script_dir = "Z:/mira"
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import nuke
from libs import get_parent_dir
# global get hud, for display hud, don't delete it.
from nuke_hud.get_hud import get_hud


class Utility(object):

    @staticmethod
    def replace_path(path):
        final_path = path.replace('\\', '/')
        return final_path


class NukePipeline(object):
    def __init__(self):
        self.parent_dir = get_parent_dir.get_parent_dir()
        self.icons_dir = os.path.join(self.parent_dir, 'icons')
        self.gizmo_dir = os.path.join(self.parent_dir, 'gizmo')
        self.conf_path = os.path.join(self.parent_dir, 'conf', 'nuke_menu.xml')

        self.add_gizmo_plugin_dir()

    def add_gizmo_plugin_dir(self):
        gizmo_dir = Utility.replace_path(self.gizmo_dir)
        nuke.pluginAddPath(gizmo_dir)

    def create_menu(self, menu_type, name):
        tool_bar = nuke.menu(menu_type)
        menu_icon = os.path.join(self.icons_dir, 'menu_icons/%s.png' % name)
        menu = tool_bar.addMenu(name, icon=menu_icon)
        return menu

    def add_cell_gizmo(self, menu, gizmo_name):
        icon_path = os.path.join(self.icons_dir, 'gizmo_icons/%s.png' % gizmo_name)
        icon_path = Utility.replace_path(icon_path)
        if os.path.isfile(icon_path):
            menu.addCommand(gizmo_name, "nuke.createNode(\"%s\")" % gizmo_name, icon=icon_path)
        else:
            menu.addCommand(gizmo_name, "nuke.createNode(\"%s\")" % gizmo_name)

    def add_pipeline_gizmo(self):
        menu = self.create_menu("Nodes", "PipelineGizmo")
        for gizmo in os.listdir(self.gizmo_dir):
            gizmo = os.path.splitext(gizmo)[0]
            self.add_cell_gizmo(menu, gizmo)

    def add_tools(self):
        tree = ET.parse(Utility.replace_path(self.conf_path))
        root = tree.getroot()
        for child in root:
            child_attr = child.attrib
            menu_type = child_attr.get("type")
            menu_name = child.get("name")
            menu = self.create_menu(menu_type, menu_name)
            for sub_menu in child:
                sub_menu_attr = sub_menu.attrib
                sub_menu_type = sub_menu_attr.get("type")
                if sub_menu_type == "separator":
                    menu.addSeparator()
                elif sub_menu_type == "command":
                    name = sub_menu_attr.get("name")
                    command = sub_menu_attr.get("command")
                    shortcut = sub_menu_attr.get("shortcut")
                    menu.addCommand(name, command, shortcut)
                else:
                    pass


def main():
    np = NukePipeline()
    np.add_pipeline_gizmo()
    np.add_tools()


if __name__ == '__main__':
    main()



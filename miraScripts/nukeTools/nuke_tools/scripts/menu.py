# -*- coding: utf-8 -*-
import os
import xml.dom.minidom
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import nuke
import get_parent_dir
reload(get_parent_dir)


class Utility(object):

    @staticmethod
    def replace_path(path):
        final_path = path.replace('\\', '/')
        return final_path


class AasNukeTool(object):
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

    def add_gizmo(self):
        menu = self.create_menu("Nodes", "Gizmo")
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
                    exec("import {0};reload({0})".format(command))
                    menu.addCommand(name, eval("%s.main" % command), shortcut)
                else:
                    pass

    @staticmethod
    def knob_default():
        nuke.knobDefault("Read.label",
                         "<font size=\"4\" color =#548DD4><b> Frame range :</b></font> "
                         "<font color = red>[value first] - [value last] </font>")


def main():
    ant = AasNukeTool()
    ant.knob_default()
    ant.add_gizmo()
    ant.add_tools()


if __name__ == '__main__':
    main()

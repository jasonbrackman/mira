# -*- coding: utf-8 -*-
import os
from get_engine import get_engine
from PySide import QtGui


class MayaAbcExpoter(object):
    def __init__(self, abc_path):
        self.abc_path = abc_path

    def export(self):
        import maya.cmds as mc
        selected = mc.ls(sl=1)
        if not selected:
            QtGui.QMessageBox.critical(None, "Error", "Nothing Selected.")
            raise RuntimeError("Select something to export.")
        root = selected[0]
        tar_dir = os.path.dirname(self.abc_path)
        if not os.path.isdir(tar_dir):
            os.makedirs(tar_dir)
        if not mc.pluginInfo("AbcExport.mll", q=1, l=1):
            mc.loadPlugin("AbcExport.mll")
        j_base_string = "-frameRange {start_frame} {end_frame} -worldSpace" \
                        " -writeVisibility -file {abc_path} -root {root}"
        j_base_string += " -uvWrite"
        j_base_string += " -renderableOnly"
        j_string = j_base_string.format(start_frame=0, end_frame=0,
                                        abc_path=self.abc_path, root=root)
        print j_string
        mc.AbcExport(j=j_string)


class AbcExporter(object):
    def __init__(self, abc_path):
        self.engine = get_engine()
        self.abc_path = abc_path

    def export(self):
        if self.engine == "maya":
            exporter = MayaAbcExpoter(self.abc_path)
        elif self.engine == "houdini":
            print "add houdini export abc method"
            # todo add houdini export abc method.
            pass
        else:
            pass
        exporter.export()

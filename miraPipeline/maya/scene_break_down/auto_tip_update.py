# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import pymel.core as pm
import scene_break_down
from miraLibs.mayaLibs import MayaTimer, get_maya_globals, get_maya_win
from miraLibs.pyLibs import get_latest_version


Settings = QSettings("Mira", "SceneBreakDownTimer")


def has_update():
    references = pm.listReferences()
    if not references:
        return
    for ref in references:
        ref_path = ref.path.replace("/", "\\")
        latest_path_versions = get_latest_version.get_latest_version(ref_path)
        if not latest_path_versions:
            continue
        latest_path = latest_path_versions[0]
        latest_path = latest_path.replace("/", "\\")
        if ref_path != latest_path:
            return True


def auto_tip_update():

    scene_break_down_timer = MayaTimer.MayaTimer()
    duration_value = Settings.value("duration")
    if not duration_value:
        Settings.setValue("duration", 20)
        duration_value = 20
    scene_break_down_timer.duration = duration_value

    def tip_update():
        if has_update():
            sbd = scene_break_down.SceneBreakDown(get_maya_win.get_maya_win("PySide"))
            sbd.close_signal.connect(scene_break_down_timer.restart)
            sbd.show()

    scene_break_down_timer.slot = tip_update
    maya_globals = get_maya_globals.get_maya_globals()
    maya_globals.add(scene_break_down_timer=scene_break_down_timer)
    scene_break_down_timer.start()


if __name__ == "__main__":
    pass

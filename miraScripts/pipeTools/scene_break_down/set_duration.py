# -*- coding: utf-8 -*-
import logging
import PySide.QtCore as QtCore
import miraLibs.mayaLibs.get_maya_globals as get_maya_globals


Settings = QtCore.QSettings("Mira", "SceneBreakDownTimer")


def set_duration(value):
    if not isinstance(value, int):
        logging.error("Duration must a type of int")
        return
    Settings.setValue("duration", value)
    maya_globals = get_maya_globals.get_maya_globals()
    timer = maya_globals.get("scene_break_down_timer")
    # set timer duration
    timer.stop()
    timer.duration = value
    timer.start()

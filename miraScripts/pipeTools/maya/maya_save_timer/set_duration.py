# -*- coding: utf-8 -*-
import logging
import PySide.QtCore as QtCore
import miraLibs.mayaLibs.get_maya_globals as get_maya_globals

logger = logging.getLogger(__name__)


Settings = QtCore.QSettings("OddOrange", "MayaSaveTimer")


def set_duration(value):
    if not isinstance(value, int):
        logger.warning("duration must be a int number.")
        return
    Settings.setValue("duration", value)
    # get current timer obj
    maya_globals = get_maya_globals.get_maya_globals()
    timer = maya_globals.get("save_timer")
    # set timer duration
    timer.stop()
    timer.duration = value
    timer.start()

if __name__ == "__main__":
    pass

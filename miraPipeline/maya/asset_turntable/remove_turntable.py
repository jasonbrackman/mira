# -*- coding: utf-8 -*-
import pymel.core as pm


def remove_turntable():
    check_group = pm.objExists('tt_rotation')
    check_camera = pm.objExists('tt_camera')
    if check_group or check_camera:
        # diag = pm.confirmDialog(title="Turn Table Detected", message="Cleaning out the turntable for Publish")
        # if diag == 'Confirm' or 'Dismiss':
        if check_camera:
            pm.delete('tt_camera')
        if check_group:
            children = pm.listRelatives('tt_rotation')
            for child in children:
                pm.parent(child, w=True)
            pm.delete('tt_rotation')


if __name__ == "__main__":
    remove_turntable()

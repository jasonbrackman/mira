# -*- coding: utf-8 -*-
import pymel.core as pm


def remove_turntable():
    check_group = pm.objExists('tt_rotation')
    if check_group:
        # diag = pm.confirmDialog(title="Turn Table Detected", message="Cleaning out the turntable for Publish")
        # if diag == 'Confirm' or 'Dismiss':
        children = pm.listRelatives('tt_rotation')
        for child in children:
            pm.parent(child, w=True)
        pm.delete('tt_rotation')


if __name__ == "__main__":
    remove_turntable()

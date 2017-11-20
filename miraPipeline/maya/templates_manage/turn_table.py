# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from miraLibs.pipeLibs import Project
from miraLibs.pipeLibs.pipeMaya import get_current_project
import os
import maya.cmds as mc


def reference_turntable():
    current_project = get_current_project.get_current_project()
    current_root = Project(current_project).primary
    turn_table_template_path = "%s/%s/templates/turnTable/turn_table.mb" % (current_root, current_project)
    if os.path.isfile(turn_table_template_path):
        mc.file(turn_table_template_path, r=1, namespace='turntable')
    else:
        mc.confirmDialog(title='Error', message='turn table not exists')

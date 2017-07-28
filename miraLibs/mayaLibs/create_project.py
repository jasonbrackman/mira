# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds
import maya.mel as mel


def create_folder(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


def create_project(project_dir):
    create_folder(project_dir)
    mel.eval('setProject \"' + project_dir + '\"')
    for file_rule in cmds.workspace(query=True, fileRuleList=True):
        file_rule_dir = cmds.workspace(fileRuleEntry=file_rule)
        maya_file_rule_dir = os.path.join(project_dir, file_rule_dir)
        create_folder(maya_file_rule_dir)

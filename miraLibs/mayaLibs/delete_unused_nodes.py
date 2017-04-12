# -*- coding: utf-8 -*-
import maya.mel as mel


def delete_unused_nodes():
    mel.eval("MLdeleteUnused;")

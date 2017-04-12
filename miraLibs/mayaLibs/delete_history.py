# -*- coding: utf-8 -*-
import maya.cmds as mc


def delete_history(sel=None):
    if sel:
        mc.delete(sel, constructionHistory=1)
    else:
        mc.delete(all=1, constructionHistory=1)

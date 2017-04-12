#!/usr/bin/env python
# coding=utf-8
# __author__ = "heshuai"
# description="""  """

import maya.cmds as mc


def undo(func):
    def _undo(*args, **kwargs):
        try:
            mc.undoInfo(ock=1)
            result = func(*args, **kwargs)
        except Exception, e:
            raise e
        else:
            return result
        finally:
            mc.undoInfo(cck=1)
    return _undo
# -*- coding: utf-8 -*-
import maya.cmds as mc


def undo(func):
    def _undo(*args, **kwargs):
        import maya.cmds as mc
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

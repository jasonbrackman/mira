# -*- coding: utf-8 -*-
import maya.cmds as mc


def set_renderer(renderer):
    mc.setAttr('defaultRenderGlobals.currentRenderer', renderer, type='string')
    if renderer == 'arnold':
        import mtoa
        mtoa.core.createOptions()


if __name__ == "__main__":
    pass

__author__ = 'heshuai'


import maya.cmds as mc
import pymel.core as pm
import mtoa.aovs as aovs
import re


def get_all_aov_list():
    aov_lists = []
    for sg in pm.ls(type='shadingEngine'):
        for aov in sg.aiCustomAOVs:
            aov_lists.append(aov.aovName.get())
    if pm.ls(type='aiWriteColor'):
        for wc in pm.ls(type='aiWriteColor'):
            m = re.compile('(.*) \(Inactive\)').match(wc.aovName.get())
            if m:
                aov_lists.append(m.groups()[0])
            else:
                if wc.aovName.get():
                    aov_lists.append(wc.aovName.get())
    aov_lists = list(set(aov_lists))
    return aov_lists


def get_aov_names():
    aov_names = [i.name for i in aovs.getAOVs()]
    return aov_names


def delete_all_aov():
    if get_all_aov_list():
        aovs.AOVInterface().removeAOVs(get_all_aov_list())


def rebuild_arnold_aov():
    for aov in get_all_aov_list():
        if aov:
            if aov not in get_aov_names():
                try:
                    aovs.AOVInterface().addAOV(aov)
                except:pass


def add_aov(aov_name):
    aov_names = [i.name for i in aovs.getAOVs()]
    if aov_name not in aov_names:
        try:
            aovs.AOVInterface().addAOV(aov_name)
        except:pass


def set_aov_enabled(status):
    aov_names = mc.ls(type='aiAOV')
    if aov_names:
        for aov_name in aov_names:
            mc.setAttr('%s.enabled' % aov_name, status)


def set_aov_enabled_adjust(status):
    current_render_layer = mc.editRenderLayerGlobals(currentRenderLayer=1, q=1)
    if current_render_layer == 'defaultRenderLayer':
        set_aov_enabled(status)
    else:
        aov_names = mc.ls(type='aiAOV')
        if aov_names:
            for aov_name in aov_names:
                mc.editRenderLayerAdjustment("%s.enabled" % aov_name)
                mc.setAttr('%s.enabled' % aov_name, status)


def remove_layer_override():
    current_render_layer = mc.editRenderLayerGlobals(currentRenderLayer=1, q=1)
    if current_render_layer != 'defaultRenderLayer':
        aov_names = mc.ls(type='aiAOV')
        if aov_names:
            for aov_name in aov_names:
                mc.editRenderLayerAdjustment('%s.enabled' % aov_name, remove=1)
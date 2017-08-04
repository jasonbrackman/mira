# -*- coding: utf-8 -*-
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile
from miraLibs.mayaLibs import open_file


assets = [u'SSWHwovenbag', u'SSWHpiano', u'SSWHpianostool', u'SSWHironbox', u'SSWHpaperbox', u'SSWHvase', u'SSWHrottencarton', u'SSWHleathersuitcaseA', u'SSWHleathersuitcaseB', u'SSWHstorageboxA', u'SSWHstorageboxB', u'SSWHstorageboxC', u'SSWHstorageboxD', u'SSWHstorageboxE', u'SSWHstorageboxF', u'SSWHbooksA', u'SSWHbooksB', u'SSWHbooksC', u'SSWHbooksD', u'SSWHbooksE', u'SSWHbooksF', u'SSWHbooksG', u'SSWHbooksH', u'SSWHbooksI', u'SSWHbooksJ', u'SSWHplasticcrate', u'SSWHstickerA', u'SSWHstickerB', u'SSWHstickerC', u'SSWHstringbag', u'SSWHtoyball', u'SSWHphotoframe', u'SSWHshoebox', u'SSWHcartonA', u'SSWHcartonB', u'SSWHcartonC', u'SSWHcartonD', u'SSWHcartonE', u'SSWHcartonF', u'SSWHcartonG', u'SSWHcartonH', u'SSWHcartonJ', u'SSWHcartonK', u'SSWHcartonL', u'SSWHcartonM', u'SSWHcartonN', u'SSOSmailbox', u'SSOSpowerdistributionbox', u'SSWHwoodA', u'SSWHwoodB', u'SSWHwoodC', u'TdTest', u'TdTest', u'SSWRlittleglasspot', u'SSWRcloset', u'SSWRpylons', u'SSWRglasspotB', u'SSWRglasspotA', u'SSWRfoodbasket', u'SSWRcookingbench', u'SSWRcabinet']


for asset in assets:
    ad_file = pipeFile.get_asset_AD_file("SnowKidTest", "Prop", asset)
    open_file.open_file(ad_file)
    ad_node = "prop_%s_AD" % asset
    all_representation = mc.assembly(ad_node, q=1, listRepresentations=1)
    for rep in all_representation:
        if rep in ["MidRig", "HighRig"]:
            mc.assembly(ad_node, edit=True, deleteRepresentation=rep)
            new_path = pipeFile.get_task_publish_file("SnowKidTest", "Asset", "Prop", asset, rep, rep)
            mc.assembly(ad_node, e=1, createRepresentation="Scene", repName=rep, input=new_path)
            all_representation = mc.assembly(ad_node, q=1, listRepresentations=1)
            index = all_representation.index(rep)
            if rep:
                mc.setAttr("%s.rep[%s].rla" % (ad_node, index), rep, type="string")

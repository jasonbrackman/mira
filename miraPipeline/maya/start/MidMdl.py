# -*- coding: utf-8 -*-
import logging
import maya.cmds as mc
from miraLibs.mayaLibs import new_file, save_as, create_group, quit_maya
from miraLibs.pipeLibs import pipeFile


def main(file_name):
    logger = logging.getLogger("MidMdl start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    asset_type = context.asset_type
    asset_name = context.asset_name
    asset_type_short_name = context.asset_type_short_name
    model_name = "%s_%s_MODEL" % (asset_type_short_name, asset_name)
    # create default group
    mc.group(name=model_name, empty=1)
    poly_group = "%s_%s_POLY" % (asset_type_short_name, asset_name)
    create_group.create_group(poly_group, model_name)
    backup_group = "%s_%s_BACKUP" % (asset_type_short_name, asset_name)
    create_group.create_group(backup_group, model_name)
    if asset_type == "Character":
        hair_mdl_grp = "hair_model_grp"
        create_group.create_group(hair_mdl_grp, backup_group)
        brow_grp = "brow_grp"
        create_group.create_group(brow_grp, backup_group)
        left_brow_grp = "left_brow_grp"
        create_group.create_group(left_brow_grp, brow_grp)
        right_brow_grp = "right_brow_grp"
        create_group.create_group(right_brow_grp, brow_grp)
        eyelash_grp = "eyelash_grp"
        create_group.create_group(eyelash_grp, backup_group)
        left_eyelash_grp = "left_eyelash_grp"
        create_group.create_group(left_eyelash_grp, eyelash_grp)
        right_eyelash_grp = "right_eyelash_grp"
        create_group.create_group(right_eyelash_grp, eyelash_grp)
        cloth_low_grp = "cloth_low_grp"
        create_group.create_group(cloth_low_grp, backup_group)

        body_group = "body_grp"
        create_group.create_group(body_group, poly_group)
        mouth_group = "mouth_grp"
        create_group.create_group(mouth_group, poly_group)
        gums_grp = "gums_grp"
        create_group.create_group(gums_grp, mouth_group)
        up_gums_grp = "up_gums_grp"
        create_group.create_group(up_gums_grp, gums_grp)
        down_gums_grp = "down_gums_grp"
        create_group.create_group(down_gums_grp, gums_grp)
        eye_group = "eye_grp"
        create_group.create_group(eye_group, poly_group)
        left_eyeball_grp = "left_eyeball_grp"
        create_group.create_group(left_eyeball_grp, eye_group)
        right_eyeball_grp = "right_eyeball_grp"
        create_group.create_group(right_eyeball_grp, eye_group)
        left_eyeball_inside_grp = "left_eyeball_inside_grp"
        create_group.create_group(left_eyeball_inside_grp, eye_group)
        right_eyeball_inside_grp = "right_eyeball_inside_grp"
        create_group.create_group(right_eyeball_inside_grp, eye_group)
        cloth_up_grp = "cloth_up_grp"
        create_group.create_group(cloth_up_grp, poly_group)
        cloth_down_grp = "cloth_down_grp"
        create_group.create_group(cloth_down_grp, poly_group)
        shoe_grp = "shoe_grp"
        create_group.create_group(shoe_grp, poly_group)
        left_shoe_grp = "left_shoe_grp"
        create_group.create_group(left_shoe_grp, shoe_grp)
        right_shoe_grp = "right_shoe_grp"
        create_group.create_group(right_shoe_grp, shoe_grp)
        other_grp = "other_grp"
        create_group.create_group(other_grp, poly_group)
    # create network node
    save_as.save_as(file_name)
    logger.info("%s publish successful!" % file_name)
    quit_maya.quit_maya()

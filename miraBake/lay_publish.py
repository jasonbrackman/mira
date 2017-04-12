# -*- coding: utf-8 -*-
import time
import logging
import optparse
import maya.cmds as mc
from miraLibs.pipeLibs import pipeFile, pipeMira
from miraLibs.mayaLibs import save_as, open_file, quit_maya, delete_all_lights, ReferenceUtility, export_abc
from miraLibs.pipeLibs.backup import backup
from miraLibs.pyLibs import copy, create_parent_dir, join_path
from miraLibs.pipeLibs.pipeDb import sql_api
from miraLibs.pipeLibs.pipeMaya.network import delete_network
from miraLibs.pipeLibs.pipeMaya.rebuild_scene import export_scene


def main():
    logger = logging.getLogger("lay publish")
    file_path = options.file
    open_file.open_file(file_path)
    # get paths
    obj = pipeFile.PathDetails.parse_path(file_path)
    seq = obj.seq
    project = obj.project
    publish_path = obj.publish_path
    camera_path = obj.camera_path
    preAnim_dir = obj.preAnim_dir
    connection_path = obj.connection_path
    tempGeo_path = obj.tempGeo_path
    # export all cameras(sequencer)
    sequencer = "sequencer_%s" % seq
    if not mc.objExists(sequencer):
        raise ValueError("%s is not exist." % sequencer)
    mc.select(clear=1)
    mc.select(sequencer, replace=1)
    mc.file(camera_path, exportSelected=1, type="mayaBinary", f=1, options="v=0", preserveReferences=1)
    logger.info("Export camera to %s" % camera_path)
    backup.backup(project, camera_path)
    # export connection .yml data
    export_scene.export_scene("sceneset", connection_path)
    logger.info("Export yml data to %s" % connection_path)
    backup.backup(project, connection_path)
    # split as anim files
    shot_obj = mc.ls(type="shot")
    for shot in shot_obj:
        shot_name = shot.split("_")[-1]
        file_base_name = pipeMira.get_shot_file_name(project)
        file_name = file_base_name.format(project_name=project, sequence=seq, shot=shot_name,
                                          category="anim", version="000")
        anim_file = join_path.join_path2(preAnim_dir, file_name)
        mc.select(clear=1)
        select_groups = ["sceneset", "prop", "char", "_REF", shot]
        mc.select(select_groups, r=1)
        mc.file(anim_file, exportSelected=1, type="mayaBinary", f=1, options="v=0", preserveReferences=1)
        logger.info("Create pre animation file: %s" % anim_file)
    logger.info("Create pre animation files done.")
    # replace workarea v000
    workarea_file_path = file_path.replace("_QCPublish", "_workarea")
    # backup.backup(project, workarea_file_path, False)
    copy.copy(file_path, workarea_file_path)
    logger.info("Cover %s" % workarea_file_path)
    # add to database
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    task_id = int(mc.getAttr("ROOT.task_id"))
    db = sql_api.SqlApi(project)
    arg_dict = {'taskId': task_id, 'taskEndDate': current_time}
    db.releaseTask(arg_dict)
    logger.info("Add to data base.")
    # save to publish path
    delete_all_lights.delete_all_lights()
    delete_network.delete_network()
    create_parent_dir.create_parent_dir(publish_path)
    save_as.save_as(publish_path)
    logger.info("Save to %s" % publish_path)
    backup.backup(project, publish_path, False)
    # import reference
    ru = ReferenceUtility.ReferenceUtility()
    ru.import_loaded_ref()
    # export temp group
    if not mc.objExists("_TEMP"):
        raise ValueError("_TEMP is not exist.")
    export_abc.export_abc(1, 1, tempGeo_path, "_TEMP")
    logger.info("Export _TEMP to %s" % tempGeo_path)
    backup.backup(project, tempGeo_path)
    # quit maya
    quit_maya.quit_maya()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="file", help="maya file ma or mb.", metavar="string")
    parser.add_option("-c", dest="command",
                      help="Not a needed argument, just for mayabatch.exe, " \
                           "if missing this setting, optparse would " \
                           "encounter an error: \"no such option: -c\"",
                      metavar="string")
    options, args = parser.parse_args()
    if len([i for i in ["file_name"] if i in dir()]) == 1:
        options.file = file_name
        main()

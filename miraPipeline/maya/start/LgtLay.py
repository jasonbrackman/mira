# -*- coding: utf-8 -*-
import glob
import logging
from miraLibs.mayaLibs import new_file, save_as, import_abc, quit_maya
from miraLibs.pipeLibs import pipeFile
from miraLibs.pipeLibs.pipeMaya import fix_frame_range


def main(file_name, local):
    logger = logging.getLogger("LgtLay start")
    new_file.new_file()
    context = pipeFile.PathDetails.parse_path(file_name)
    # fix frame range
    fix_frame_range.fix_frame_range(context)
    # get the AnimLay cache
    abc_files = get_cache_files(context)
    if abc_files:
        for abc_file in abc_files:
            import_abc.import_abc(abc_file)
        save_as.save_as(file_name)
        logger.info("%s publish successful!" % file_name)
    if not local:
        quit_maya.quit_maya()


def get_cache_files(context):
    AnimLay_publish_file = pipeFile.get_task_publish_file(context.project, "Shot", context.sequence,
                                                          context.shot, "AnimLay", "AnimLay")
    AnimLay_context = pipeFile.PathDetails.parse_path(AnimLay_publish_file)
    cache_dir = AnimLay_context.cache_dir
    abc_files = glob.glob("%s/*.abc" % cache_dir)
    return abc_files

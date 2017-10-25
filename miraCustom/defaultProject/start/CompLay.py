# -*- coding: utf-8 -*-
import logging
import nuke
from miraLibs.nukeLibs import new_file, save_as, quit_nuke
from miraLibs.pipeLibs import pipeFile


def main(file_name, local):
    logger = logging.getLogger("CompLay start")
    # new scene
    new_file.new_file()
    # create write node
    context = pipeFile.PathDetails.parse_path(file_name)
    render_path = context.render_output
    write_node = nuke.nodes.Write(name="Final_Render", file=render_path, postage_stamp=True, file_type=10)
    write_node.knob("datatype").setValue(1)
    logger.info("Create Write node done.")
    # save as file name
    save_as.save_as(file_name)
    if not local:
        quit_nuke.quit_nuke()

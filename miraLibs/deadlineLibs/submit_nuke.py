# -*- coding: utf-8 -*-
import sys
import nuke
import pipeGlobal
import DeadlineSubmission
reload(DeadlineSubmission)
from DeadlineSubmission import DeadlineSubmission
from miraLibs.pipeLibs import pipeFile


def get_render_py():
    lib_dir = pipeGlobal.libs_dir
    render_py = "%s/pipeLibs/pipeNuke/render.py" % lib_dir
    return render_py


def submit_nuke():
    filein = nuke.root().name()
    context = pipeFile.PathDetails.parse_path(filein)
    # dets = pft.PathDetails.parse_path(pm.sceneName())
    # fileout = dets.getRenderFullPath().split('.####.')[0]
    # pm.setAttr('defaultRenderGlobals.imageFilePrefix', fileout)
    nuke_exe = sys.executable
    name = "nuke_%s_%s_%s_%s" % (context.project, context.sequence, context.shot, context.step)
    # comment = ''
    render_py = get_render_py()
    maya_args = '-t %s %s' % (render_py, filein)

    sub = DeadlineSubmission()
    sub.setExe(nuke_exe)
    sub.setArgs(maya_args)
    sub.setName(name)
    sub.setChunkSize(1)
    sub.submit()

    nuke.message("Submit Done.")

# -*- coding: utf-8 -*-
import os
import sys
import pymel.core as pm
import maya.mel as mel
import DeadlineSubmission
reload(DeadlineSubmission)
from DeadlineSubmission import DeadlineSubmission
from miraLibs.pyLibs import copy
from miraLibs.pipeLibs import pipeFile


def submit_maya():
    context = pipeFile.PathDetails.parse_path(pm.sceneName())
    output_file_path = context.render_output
    # this will submit a job to deadline with the current maya scene's settings. It's just a placeholder at the moment
    # until we get our GUI up and running with this style of command line submission.
    driver, suffix = os.path.splitdrive(pm.sceneName())
    filein = "R:%s" % suffix
    mel.eval('setMayaSoftwareFrameExt(3,0);')
    pm.saveFile(f=1)
    copy.copy(pm.sceneName(), filein)
    # dets = pft.PathDetails.parse_path(pm.sceneName())
    # fileout = dets.getRenderFullPath().split('.####.')[0]
    # pm.setAttr('defaultRenderGlobals.imageFilePrefix', fileout)
    maya_dir = os.path.dirname(sys.executable)
    maya_exex = '%s\Render.exe' % maya_dir
    start_frame = int(pm.playbackOptions(animationStartTime=True, query=True))
    end_frame = int(pm.playbackOptions(animationEndTime=True, query=True))
    name = "maya_%s_%s_%s_%s" % (context.project, context.sequence, context.shot, context.step)
    # comment = ''

    maya_args = '-s <STARTFRAME>  -e <ENDFRAME>  -rd %s %s ' % (output_file_path, filein)

    sub = DeadlineSubmission()
    sub.setExe(maya_exex)
    sub.setArgs(maya_args)
    sub.setName(name)
    sub.setFrames("%s-%s" % (start_frame, end_frame))
    sub.setChunkSize(1)
    sub.submit()


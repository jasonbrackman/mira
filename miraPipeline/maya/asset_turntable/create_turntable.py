# -*- coding: utf-8 -*-
import logging
import pymel.core as pm
import maya.cmds as mc
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI


def bounding_by_frame(frame_range=[], path=[]):
    if len(frame_range) == 2:
        if path is not None:
            path = mc.ls(path)
            boundingbox = [999999999, 999999999, 999999999, -999999999, -999999999, -999999999]
            for frame in range(frame_range[0], frame_range[1]+1):
                mc.currentTime(frame)
                temp = mc.exactWorldBoundingBox(path)
                if boundingbox[0] > temp[0]:
                    boundingbox[0] = temp[0]
                if boundingbox[1] > temp[1]:
                    boundingbox[1] = temp[1]
                if boundingbox[2] > temp[2]:
                    boundingbox[2] = temp[2]
                if boundingbox[3] < temp[3]:
                    boundingbox[3] = temp[3]
                if boundingbox[4] < temp[4]:
                    boundingbox[4] = temp[4]
                if boundingbox[5] < temp[5]:
                    boundingbox[5] = temp[5]
           
            return boundingbox


def create_warp_box_bounding(bbox=[]):
    if bbox is not None:
        points = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        if len(bbox) == 6:
            points[0] = [bbox[0], bbox[1], bbox[5]]
            points[1] = [bbox[3], bbox[1], bbox[5]]
            points[2] = [bbox[0], bbox[4], bbox[5]]
            points[3] = [bbox[3], bbox[4], bbox[5]]
            points[4] = [bbox[0], bbox[4], bbox[2]]
            points[5] = [bbox[3], bbox[4], bbox[2]]
            points[6] = [bbox[0], bbox[1], bbox[2]]
            points[7] = [bbox[3], bbox[1], bbox[2]]

        box = mc.polyCube()
        bos_shape = mc.listRelatives(box, shapes=True)[0]
        for i in range(8):
            position = mc.pointPosition('%s.vtx[%d]' % (box[0], i), world=True)
            points[i][0] -= position[0]
            points[i][1] -= position[1]
            points[i][2] -= position[2]
            mc.setAttr('%s.pnts[%d].pntx' % (bos_shape, i), points[i][0])
            mc.setAttr('%s.pnts[%d].pnty' % (bos_shape, i), points[i][1])
            mc.setAttr('%s.pnts[%d].pntz' % (bos_shape, i), points[i][2])
        return box[0]

        
def create_turntable():
    # # save current file
    # mc.file(save=1, f=1)
    # sel the group for turntable
    sel = mc.ls(sl=1)
    group_name = "tt_rotation"
    # cam_name = "tt_camera"
    if sel:
        if pm.ls(group_name):
            logging.warning("tt_rotation group exist.")
            return
        else:
            # group the sel as tt_rotation
            mc.group(n="tt_rotation")
            # mc.parent(sel, "tt_rotation")
            mc.xform("tt_rotation", rotatePivot=[0, 0, 0], worldSpace=1)
            # key the tt_rotation group
            mc.setKeyframe("tt_rotation", value=0, t=0, itt="linear", ott="linear", at="rotateY")
            mc.setKeyframe('tt_rotation', v=360, t=240, itt='linear', ott='linear', at='rotateY')
            # set animation range
            mc.playbackOptions(minTime=0, animationStartTime=0)
            mc.playbackOptions(maxTime=240, animationEndTime=240)
            bb = bounding_by_frame([0,240],['tt_rotation'])
            box = create_warp_box_bounding(bb)
            
            view = OpenMayaUI.M3dView.active3dView()
            cam = OpenMaya.MDagPath()
            view.getCamera(cam)
            camPath = cam.fullPathName()
            # look though the camera
            mc.viewFit(camPath, fitFactor=mc.getAttr('defaultResolution.pixelAspect')/mc.getAttr('defaultResolution.deviceAspectRatio'))
            
            #center = mc.objectCenter(box)
            #distance = max([abs(each) for each in bb])
            #distance *= 2.42
            
            #cam_ = mc.listRelatives(camPath,parent=True)[0]
            
            #mc.setAttr("%s.translateX" % cam_,center[0])
            #mc.setAttr("%s.translateY" % cam_,center[1])
            #mc.setAttr("%s.translateZ" % cam_,center[2])
      
            #mc.camera(camPath,e=True,centerOfInterest=distance)
            
            mc.delete(box)
            return camPath
    else:
        logging.error('No object selected, please select an object')
        return False


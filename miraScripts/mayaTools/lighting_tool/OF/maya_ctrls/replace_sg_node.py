# coding utf-8
# __author__ = "heshuai"
# description="""  """


import maya.cmds as mc
from PySide import QtGui, QtCore


def replace_sg():
    for sg in mc.ls(type='shadingEngine'):
        if sg not in ['initialParticleSE', 'initialShadingGroup']:
            new_sg = mc.createNode('shadingEngine')
            mc.nodeCast(sg, new_sg, copyDynamicAttrs=1, swapValues=1, f=1)
            try:
                mc.delete(sg)
            except:
                mc.warning('%s can not be deleted' % sg)
            else:
                mc.rename(new_sg, sg)
                print '[OF] info: %s has been replaced' % sg


def main():
    message_box = QtGui.QMessageBox()
    message_box.setIcon(QtGui.QMessageBox.Information)
    message_box.setText('information')
    message_box.setInformativeText('Do you want to replace all the sg node?')
    message_box.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
    ret = message_box.exec_()
    if ret == QtGui.QMessageBox.Yes:
        import rebulid_arnold_aov
        reload(rebulid_arnold_aov)
        rebulid_arnold_aov.rebuild_arnold_aov()
        print "[OF] info: rebuild aov finished"
        replace_sg()


if __name__ == '__main__':
    main()



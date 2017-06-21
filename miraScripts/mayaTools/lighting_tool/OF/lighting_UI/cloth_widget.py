# coding=utf-8
# __author__ = "heshuai"
# description="""  """
import pymel.core as pm
import re
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import sys
import public_ctrls
from public_ctrls import warm_tip
import time
from maya_ctrls import shading_group_operation



pattern_hair = re.compile(r'.*((toufa)|([fF]ur)|([hH]air))$')
pattern_cloth = re.compile(r'(.*:)?(.*:.*)_clo(th)?Fix$')


def get_transform():
    transforms = [transform for transform in pm.ls(type='transform') if transform.getShape()]
    return transforms


def hide_object(transform_node):
    try:
        transform_node.visibility.set(0)
    except:
        if transform_node.visibility.isLocked():
            transform_node.visibility.setLocked(0)
        if transform_node.visibility.connections():
            try:
                attrs = pm.listConnections(transform_node.visibility, plugs=1)
                for attr in attrs:
                    pm.disconnectAttr(attr, transform_node.visibility)
                transform_node.visibility.set(0)
            except Exception as e:
                print "[OF] <hide error> : %s" % e
        else:
            transform_node.visibility.set(0)


def hide_hair(transforms):
    hair = [transform for transform in transforms if pattern_hair.match(transform.name())]
    for i in hair:
        hide_object(i)


def get_cache_clothes_list(transforms):
    cache_clothes_list = []
    pattern = re.compile(r'(.*:)?(.*:.*)_clo(th)?Fix$')
    for transform in transforms:
        if pattern.match(transform.name()):
            if transform.getShape():
                cache_clothes_list.append([transform.name(), pattern.match(transform.name()).group(2)])
    return cache_clothes_list


def get_all_clothes(transforms):
    clothes_list = []
    cache_cloths_list = get_cache_clothes_list(transforms)
    if cache_cloths_list:
        for transform in transforms:
            for cache_clothes in cache_cloths_list:
                if transform.name().endswith(cache_clothes[1]):
                    clothes_list.append([cache_clothes[0], transform.name()])
                    break
    return clothes_list


def get_transform_node_sg(node):
    if node.getShape():
        sg_node = node.getShape().outputs(type='shadingEngine')
        try:
            sg_node.remove(pm.PyNode('initialShadingGroup'))
        except:pass
        if sg_node:
            return sg_node[0]
        else:
            return False
    else:
        return False


def auto_main():
    start = time.time()
    transforms = get_transform()
    hide_hair(transforms)
    print "[OF] info: hide hair successful!"
    clothes_list = get_all_clothes(transforms)
    for cloth in clothes_list:
        print cloth
        if len(cloth) == 2:
            try:
                shading_group_operation.assign_to_new_obj(cloth[1], cloth[0])
                #pm.sets(get_transform_node_sg(cloth[1]), fe=cloth[0])
                print "[OF] info: assign material %s ------> %s" % (cloth[1], cloth[0])
            except Exception as e:
                print "[OF] error: <assign error> %s" % e
            hide_object(pm.PyNode(cloth[1]))
    print time.time()-start


def auto_assist():
    sys.path.append(r'C:\mnt\centralized_tool\DateBag\20141015_1239\python\studio\maya\tem')
    import miarmy as bcmiarmy
    reload(bcmiarmy)
    bcmiarmy.blendCloth2()


def manu():
    if len(pm.ls(sl=1)) == 0:
        warm_tip.warm_tip('Nothing selected')
    elif len(pm.ls(sl=1)) != 2:
        warm_tip.warm_tip('Please check the number of selected meshes is 2')
    else:
        selected_objects = pm.ls(sl=1)
        if not selected_objects[1].name().endswith('Fix'):
            selected_objects.reverse()
        shading_group_operation.assign_to_new_obj(selected_objects[0].name(), selected_objects[1].name())
        #sg_node = selected_objects[0].getShape().outputs(type='shadingEngine')[0]
        #pm.sets(sg_node, fe=selected_objects[1])
        hide_object(selected_objects[0])
        print selected_objects[0]+'-------->'+selected_objects[1]


class Cloth(QDialog):
    def __init__(self, parent=None):
        super(Cloth, self).__init__(parent)
        self.setWindowTitle('Cloth')
        y_pos = public_ctrls.get_maya_main_win_pos()[1] + (public_ctrls.get_maya_main_win_size()[1])/4
        self.move(public_ctrls.get_maya_main_win_pos()[0], y_pos)
        main_layout = QVBoxLayout(self)
        auto_group = QGroupBox('Auto')
        main_layout.addWidget(auto_group)
        auto_layout = QHBoxLayout(auto_group)
        self.auto_main_btn = QPushButton('Auto Main')
        self.auto_main_btn.setFixedWidth(230)
        self.auto_assist_btn = QPushButton('Auto assist')
        auto_layout.addWidget(self.auto_main_btn)
        auto_layout.addWidget(self.auto_assist_btn)
        manu_group = QGroupBox('Manu')
        main_layout.addWidget(manu_group)
        manu_layout = QHBoxLayout(manu_group)
        self.manu_btn = QPushButton('manu')
        manu_layout.addWidget(self.manu_btn)
        self.set_signals()

    def set_signals(self):
        self.auto_main_btn.clicked.connect(auto_main)
        self.auto_assist_btn.clicked.connect(auto_assist)
        self.manu_btn.clicked.connect(manu)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()


def run():
    global mw
    try:
        mw.close()
        mw.deleteLater()
    except:pass
    mw = Cloth(public_ctrls.get_maya_win())
    mw.show()

if __name__ == '__main__':
    run()
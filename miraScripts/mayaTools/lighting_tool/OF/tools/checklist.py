# -*- coding：utf-8 -*-
# __author__ = "heshuai"
# description="""  """
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
import maya.cmds as mc
import maya.OpenMayaUI as mui
import sip

checklist_object = u'渲染提交农场之前检查的事项'


class CheckList(QDialog):
    def __init__(self, parent=None):
        super(CheckList, self).__init__(parent)
        self.setObjectName(checklist_object)
        self.setWindowTitle(checklist_object)
        self.resize(1040, 400)
        main_layout = QVBoxLayout(self)
        farm_label = QLabel(u'<font size=4 color="#fd8288"><b>渲染提交<font size=4 color="#00FF00"><b>农场<font size=4 color="#fd8288"><b>之前检查的事项')
        farm_text_edit = InfoText()
        farm_text_edit.setFixedHeight(220)
        farm_text_edit.setText(u'01. 是否跟动画、场景整合视频一致，是否有穿帮问题，摄像机是否正确\n'
                               u'02. 毛发渲染之前检查相关视频，必须和解算一致，必须匹配角色，毛发的模型是否隐藏\n'
                               u'03. 布料渲染之前检查相关视频，必须和解算一致，发现没有解算的布料及时向前面环节求证\n'
                               u'04. 动画、毛发、布料、群组前后帧是否有预留\n'
                               u'05. 确保灯光连镜\n'
                               u'06. 不得将角色和场景分开进行灯光（如遇特殊情况请TS和supervisor确认之后在进行，但也要确保角色和场景的光源方向、阴影、氛围等保持一致）\n'
                               u'07. 测试一张最终精度带AOV的小图，检查材质是否正确，贴图精度是否达到要求，有无曝光、死黑、奇怪的线、奇怪的物体等问题出现，AOV的通道用NUKE检查是否正确合理\n'
                               u'08. 测试一段低质量的带motion AOV的序列，检查是否有穿帮，motion的动态是否正确合理，细分置换是否合理，置换开启后是否有穿帮，采样的参数是否合理\n'
                               u'09. 提交农场渲染前请检查帧数、帧率、尺寸、摄像机的选择是否正确、采样是否是渲染最终质量的参数，motion、AOV、细分、置换是否开启\n'
                               u'10. 角色渲染问题：运动重叠中的角色分开渲染，不得加遮罩，有穿插的出mask\n'
                               u'11. Daily单帧的时候，如果镜头的里的动态比较大，多渲几帧进行daily，确保灯光在不同角度都适用')
        comp_label = QLabel(u'<font size=4 color="#fd8288"><b>渲染提交<font size=4 color="#00FF00"><b>后期<font size=4 color="#fd8288"><b>之前检查的事项')
        comp_text_edit = InfoText()
        comp_text_edit.setFixedHeight(200)
        comp_text_edit.setText(u'01. 必须出light_check让TS、supervisor daily通过\n'
                               u'02. 提交后期文件前必须严格检查缺帧、错帧、漏帧问题\n'
                               u'03. 通道提前出给后期（arnold的aov在asset阶段就已添加，所以在提交后期之前需要检查是否正确，道具、还有效果不好的元素还需要渲染更多的通道）\n'
                               u'04. 文件正确命名，文件存放路径正确（重新渲染的序列不得覆盖旧文件）\n'
                               u'05. 文件更替时，必须重新渲染相关联的元素\n'
                               u'06. 检查序列图的细分、置换是否正确\n'
                               u'07. 序列和通过的单帧保持一致\n'
                               u'08. 天空和场景整合通过的保持一致\n'
                               u'09. 提交的序列不得出现明显的闪烁（如有闪烁请确认是否接受）\n'
                               u'10. 贴图精度有问题需要确认，不得盲目递交')

        main_layout.addWidget(farm_label)
        main_layout.addWidget(farm_text_edit)
        main_layout.addWidget(comp_label)
        main_layout.addWidget(comp_text_edit)
        

class InfoText(QTextEdit):
    def __init__(self, parent=None):
        super(InfoText, self).__init__(parent)
        self.setEnabled(False)
        self.setStyleSheet('QTextEdit{background: #e6b399; color:#000000; font-size:13px}')
        
        
def get_maya_win():
    prt = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(prt), QWidget)
    

def run():
    if mc.window(checklist_object, q=1, exists=1):
        mc.deleteUI(checklist_object)
    cl = CheckList(get_maya_win())
    cl.show()
    
    
if __name__ == '__main__':
    run()
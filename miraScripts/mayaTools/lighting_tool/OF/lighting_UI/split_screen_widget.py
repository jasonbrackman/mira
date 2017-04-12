from PySide import QtGui, QtCore
import maya.cmds as cmds
from public_ctrls import get_maya_win

expString = '''\
// SplitScreen Expression
int $n = {0};
float $r = defaultResolution.deviceAspectRatio;
preScale = $n;
filmTranslateH = (frame % $n - ($n - 1) * 0.5) * 2;
filmTranslateV = ((trunc(frame / $n)) % $n - ($n - 1) * 0.5) / $r * 2;
'''
noteString = '''\
Enter an int: N
If N > 1,  create or edit the expression;
If N = 0, delete the expression.
'''


def get_all_cameras():
    return cmds.ls(cameras=1)
    
 
def GetActivedCamera():
    wfPanel = cmds.playblast( ae = 1)
    if cmds.getPanel(to = wfPanel) == 'modelPanel':
        camera =  cmds.modelEditor(wfPanel, q = 1, cam = 1)
        camera_shape = cmds.ls(camera, dag=1, shapes=1)[0]
        cmds.setAttr('%s.preScale' % camera_shape, lock=0)
        cmds.setAttr('%s.filmTranslate' % camera_shape, lock=0)
        return camera_shape

def GetExpression(cam):
    conns = {}
    for attr in ('preScale', 'filmTranslateH', 'filmTranslateV'):
        exp = cmds.listConnections('%s.%s' % (cam, attr), t = 'expression')
        if exp: conns[exp[0]] = 1
    if conns and len(conns) == 1: return conns.keys()[0]
    

def AddExpression(cam, num):
    cmds.expression(s = expString.format(num), o = cam, ae = 1)
    

def EditExpression(exp, num):
    cmds.expression(exp, e = 1, s = expString.format(num))
    

def DeleteExpression(cam, exp):
    cmds.delete(exp)
    cmds.setAttr('%s.preScale' % cam, 1)
    cmds.setAttr('%s.filmTranslateH' % cam, 0)
    cmds.setAttr('%s.filmTranslateV' % cam, 0)


def set_range(start, end):
    cmds.playbackOptions(e=1, min=start)
    cmds.playbackOptions(e=1, max=end) 
    cmds.setAttr('defaultRenderGlobals.startFrame', start)
    cmds.setAttr('defaultRenderGlobals.endFrame', end)


def get_start_frame():
    return cmds.playbackOptions(q=1, min=1)


def set_render_camera(camera):
    cameras = cmds.ls(type='camera')
    for cam in cameras:
        cmds.setAttr(cam+'.renderable', 0)
    cmds.setAttr(camera+'.renderable', 1)
    
        
class SplitScreen(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SplitScreen, self).__init__(parent)
        self.resize(350, 150)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('Split Screen')
        self.setObjectName('Split Screen')
        main_layout = QtGui.QVBoxLayout(self)
        self.cbox = QtGui.QComboBox()
        self.label = QtGui.QLabel()
        
        num_layout = QtGui.QHBoxLayout()
        num_label = QtGui.QLabel('Split Number(N)')
        self.le = QtGui.QLineEdit()
        num_layout.addWidget(num_label)
        num_layout.addWidget(self.le)
        
        btn_layout = QtGui.QHBoxLayout()
        self.ok_btn = QtGui.QPushButton('OK')
        self.cancel_btn = QtGui.QPushButton('Cancel')
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        frame_layout = QtGui.QHBoxLayout()
        start_label = QtGui.QLabel('Start Frame')
        self.start_le = QtGui.QLineEdit()
        end_label = QtGui.QLabel('End Frame')
        self.end_le = QtGui.QLineEdit()
        self.end_le.setEnabled(False)
        frame_layout.addWidget(start_label)
        frame_layout.addWidget(self.start_le)
        frame_layout.addWidget(end_label)
        frame_layout.addWidget(self.end_le)
        
        main_layout.addWidget(self.cbox)
        main_layout.addWidget(self.label)
        main_layout.addLayout(num_layout)
        main_layout.addLayout(frame_layout)
        main_layout.addLayout(btn_layout)
        
        self.init_settings()
        self.set_signals()
        
    def init_settings(self):
        self.label.setText(noteString)
        
        cameras = get_all_cameras()
        for camera in cameras:
            self.cbox.addItem(camera)
        need_camera = GetActivedCamera()
        if need_camera:
            index = self.cbox.findText(need_camera)
            self.cbox.setCurrentIndex(index)
        self.start_le.setText(str(get_start_frame()))
            
    def set_signals(self):
        self.ok_btn.clicked.connect(self.do_split)
        self.cancel_btn.clicked.connect(self.close)
        self.start_le.textChanged.connect(self.set_frame_range)
        self.le.textChanged.connect(self.set_frame_range_new)
        
    def set_frame_range(self, frame):
        num = self.le.text()
        if num:
            if not num.isdigit():
                cmds.error('Only <int> Allowed.')
                return 
            number = int(num)
            if frame.isdigit():
                start_frame = int(frame)
                if number != 0:
                    end_frame = start_frame + pow(number, 2) -1 
                else:
                    end_frame = start_frame
                self.end_le.setText(str(end_frame))
                set_range(start_frame, end_frame)

    def set_frame_range_new(self, num):
        if not num.isdigit():
            cmds.error('Only <int> Allowed.')
            return 
        start_frame = self.start_le.text()
        if start_frame:
            if int(num) != 0:
                end_frame = int(float(start_frame)) + pow(int(num), 2) -1
            else:
                end_frame = int(float(start_frame))
            self.end_le.setText(str(end_frame))
            set_range(start_frame, end_frame)
        
    def do_split(self):
        cam = self.cbox.currentText()
        if not cam:
            cmds.error('Camera Not Found.')
            return
        num = self.le.text()
        if not num.isdigit():
            cmds.error('Only <int> Allowed.')
            return
        set_render_camera(cam)
        num = int(num)
        exp = GetExpression(cam)
        if not exp and num > 1:
            AddExpression(cam, num)
        elif exp and num > 1:
            EditExpression(exp, num)
        elif exp and num <= 1:
            DeleteExpression(cam, exp)

    @classmethod    
    def show_ui(cls):
        if cmds.window('Split Screen', q=1, ex=1):
            cmds.deleteUI('Split Screen')
        ss = SplitScreen(get_maya_win())
        ss.show()
        
        
def main():
    SplitScreen.show_ui()

if __name__ == '__main__':
    main()
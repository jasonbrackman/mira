# coding=utf-8
# __author__ = "heshuai"
# description="""  """

from PySide import QtGui, QtCore
import pymel.core as pm
import maya.OpenMayaUI as mui
import sip


def get_maya_win():
    prt = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(prt), QtGui.QWidget)


def create_image_plane():
    if not pm.objExists('MY_IMAGE_PLANE'):
        image_plane_shape = pm.createNode('imagePlane', name='MY_IMAGE_PLANE')
        return image_plane_shape
    else:
        return pm.PyNode('MY_IMAGE_PLANE')


def connect(camera):
    image_plane_shape = create_image_plane()
    image_plane_shape.message >> camera.imagePlane[0]


class ImagePlane(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ImagePlane, self).__init__(parent)
        self.setWindowTitle('Create Image Plane')
        self.resize(400, 100)
        main_layout = QtGui.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_frame = QtGui.QFrame()
        main_layout.addWidget(main_frame)
        main_frame.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        layout_of_frame = QtGui.QVBoxLayout(main_frame)
        #--------------------image   layout -----------------------#
        image_layout = QtGui.QHBoxLayout()
        image_label = QtGui.QLabel('Image Name')
        image_label.setFixedWidth(65)
        image_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.image_le = QtGui.QLineEdit()
        self.image_btn = QtGui.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(self.style().standardPixmap(QtGui.QStyle.SP_DirOpenIcon))
        self.image_btn.setIcon(icon)
        image_layout.addWidget(image_label)
        image_layout.addWidget(self.image_le)
        image_layout.addWidget(self.image_btn)
        #--------------------      Alpha     -----------------------#
        alpha_layout = QtGui.QHBoxLayout()
        alpha_label = QtGui.QLabel('Alpha Gain')
        alpha_label.setFixedWidth(65)
        alpha_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.alpha_le = QtGui.QLineEdit()
        self.alpha_le.setFixedWidth(65)
        self.alpha_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.alpha_slider.setMinimum(0)
        self.alpha_slider.setMaximum(1)
        alpha_layout.addWidget(alpha_label)
        alpha_layout.addWidget(self.alpha_le)
        alpha_layout.addWidget(self.alpha_slider)
        #---------------------------depth-------------------------------#
        depth_layout = QtGui.QHBoxLayout()
        depth_label = QtGui.QLabel('Depth')
        depth_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        depth_label.setFixedWidth(65)
        self.depth_le = QtGui.QLineEdit()
        self.depth_le.setFixedWidth(80)
        depth_layout.addWidget(depth_label)
        depth_layout.addWidget(self.depth_le)
        depth_layout.addStretch()
        #---------------------------separator layout-------------------------------#
        separator_layout = QtGui.QHBoxLayout()
        separator_layout.setContentsMargins(0, 10, 0, 0)
        separator_layout.setAlignment(QtCore.Qt.AlignBottom)
        frame = QtGui.QFrame()
        frame.setFrameStyle(QtGui.QFrame.HLine)
        frame.setStyleSheet('QFrame{color: #111111}')
        separator_layout.addWidget(frame)
        #---------------------------create layout-------------------------------#
        create_layout = QtGui.QHBoxLayout()
        self.camera_btn = QtGui.QPushButton('Select Camera')
        self.camera_le = QtGui.QLineEdit()
        self.create_btn = QtGui.QPushButton('Create')
        create_layout.addWidget(self.camera_btn)
        create_layout.addWidget(self.camera_le)
        create_layout.addWidget(self.create_btn)
        #-----------------------------------------------------------------------#
        layout_of_frame.addLayout(image_layout)
        layout_of_frame.addLayout(alpha_layout)
        layout_of_frame.addLayout(depth_layout)
        layout_of_frame.addLayout(separator_layout)
        layout_of_frame.addLayout(create_layout)
        #------------------------------------------------------------------------#
        self.init_settings()
        self.set_signals()

    def set_signals(self):
        self.image_btn.clicked.connect(self.get_image_path)
        self.image_le.textChanged.connect(self.set_image_path)
        self.alpha_slider.valueChanged.connect(self.set_alpha)
        self.alpha_le.textChanged.connect(self.set_slider)
        self.depth_le.textChanged.connect(self.set_depth)
        self.camera_btn.clicked.connect(self.select_camera)
        self.create_btn.clicked.connect(self.do_create)

    def init_settings(self):
        if pm.objExists('MY_IMAGE_PLANE'):
            self.alpha_slider.setValue(int(pm.PyNode('MY_IMAGE_PLANE').alphaGain.get()))
            self.alpha_le.setText(str(pm.PyNode('MY_IMAGE_PLANE').alphaGain.get()))
            self.depth_le.setText(str(pm.PyNode('MY_IMAGE_PLANE').depth.get()))
            self.image_le.setText(pm.PyNode('MY_IMAGE_PLANE').imageName.get())
        else:
            self.alpha_slider.setValue(1)
            self.alpha_le.setText('1')
            self.depth_le.setText('1000')

    def get_image_path(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        file_path = file_dialog.getOpenFileName(self, 'choose the image file', '/',
                                                "Image Files (*.png *.jpg *.bmp *.hdr *.tga *.exr *.tx)")
        self.image_le.setText(file_path)

    def set_alpha(self, value):
        self.alpha_le.setText(str(value))
        if pm.objExists('MY_IMAGE_PLANE'):
            pm.PyNode('MY_IMAGE_PLANE').alphaGain.set(int(value))

    def set_slider(self, text):
        self.alpha_slider.setValue(int(float(text)))

    def set_image_path(self, text):
        if pm.objExists('MY_IMAGE_PLANE'):
            pm.PyNode('MY_IMAGE_PLANE').imageName.set(text)

    def set_depth(self, text):
        if pm.objExists('MY_IMAGE_PLANE'):
            pm.PyNode('MY_IMAGE_PLANE').depth.set(int(float(text)))

    def select_camera(self):
        if pm.ls(sl=1):
            sel = pm.ls(sl=1)[0]
            if sel.getShape().type() == 'camera':
                self.camera_le.setText(sel.getShape().name())

    def do_create(self):
        camera = None
        if self.camera_le.text():
            camera = pm.PyNode(str(self.camera_le.text()))
        image_path = str(self.image_le.text())
        depth = int(float(self.depth_le.text()))
        alpha = int(float(self.alpha_le.text()))
        if not pm.objExists('MY_IMAGE_PLANE'):
            if camera:
                connect(camera)
        try:
            pm.PyNode('MY_IMAGE_PLANE').alphaGain.set(alpha)
            pm.PyNode('MY_IMAGE_PLANE').depth.set(depth)
            pm.PyNode('MY_IMAGE_PLANE').imageName.set(image_path)
        except:pass
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.close()

def main():
    global ip
    try:
        ip.close()
        ip.deleteLater()
    except:pass
    ip = ImagePlane(get_maya_win())
    ip.show()


if __name__ == '__main__':
    main()
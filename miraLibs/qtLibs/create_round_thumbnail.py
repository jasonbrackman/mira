# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore


def create_round_thumbnail(image_path, scale_size):
    """
    Create a custom px wide circle thumbnail
    :param image_path: a png file path
    :param scale_size: scale size of the image
    :return: QPixmap
    """
    # get the 512 base image
    base_image = QtGui.QPixmap(scale_size, scale_size)
    base_image.fill(QtCore.Qt.transparent)
    # now attempt to load the image
    image = QtGui.QImage(image_path)
    thumb = QtGui.QPixmap.fromImage(image)
    # pixmap will be a null pixmap if load fails
    if not thumb.isNull():
        # scale it down to fit inside a frame of maximum 512x512
        thumb_scaled = thumb.scaled(scale_size,
                                    scale_size,
                                    QtCore.Qt.KeepAspectRatioByExpanding,
                                    QtCore.Qt.SmoothTransformation)

        # now composite the thumbnail on top of the base image
        # bottom align it to make it look nice
        thumb_img = thumb_scaled.toImage()
        brush = QtGui.QBrush(thumb_img)
        painter = QtGui.QPainter(base_image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(0, 0, scale_size, scale_size)
        painter.end()

    return base_image


class Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        main_layout = QtGui.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QtGui.QLabel()
        main_layout.addWidget(self.label)
        self.draw()

    def draw(self):
        pix_map = create_round_thumbnail(r"D:\pictures\CG\micheal.png", 200)
        self.label.setPixmap(pix_map)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())













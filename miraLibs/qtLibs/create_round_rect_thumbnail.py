# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


def create_round_rect_thumbnail(image_path, scale_width, scale_height, border_radius):
    """
    Create a custom px wide round rect thumbnail
    :param image_path: a png file path
    :param scale_width: scale width of the image
    :param scale_height: scale height of the image
    :param border_radius: the border radius of the image
    :return:
    """
    # get the 512 base image
    base_image = QPixmap(scale_width, scale_height)
    base_image.fill(Qt.transparent)
    # now attempt to load the image
    image = QImage(image_path)
    thumb = QPixmap.fromImage(image)
    # pixmap will be a null pixmap if load fails
    if not thumb.isNull():
        # scale it down to fit inside a frame of maximum 512x512
        thumb_scaled = thumb.scaled(scale_width,
                                    scale_height,
                                    Qt.IgnoreAspectRatio,
                                    Qt.SmoothTransformation)

        # now composite the thumbnail on top of the base image
        # bottom align it to make it look nice
        thumb_img = thumb_scaled.toImage()
        brush = QBrush(thumb_img)
        painter = QPainter(base_image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        rect = QRectF(0, 0, scale_width, scale_height)
        painter.drawRoundRect(rect, border_radius, border_radius)             
        painter.end()
    
    return base_image


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel()
        main_layout.addWidget(self.label)
        self.draw()
        
    def draw(self):
        pix_map = create_round_rect_thumbnail(r"D:\pictures\CG\env.png", 200, 200, 20)
        self.label.setPixmap(pix_map)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())

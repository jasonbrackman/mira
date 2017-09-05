from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *


class TaskUI(QDialog):
    def __init__(self, text, model_data, parent=None):
        super(TaskUI, self).__init__(parent)
        self.text = text
        self.model_data = model_data
        self.resize(450, 500)
        main_layout = QVBoxLayout(self)
        self.entity_label = QLabel()
        self.list_view = QListView()
        self.list_view.setSpacing(2)
        main_layout.addWidget(self.entity_label)
        main_layout.addWidget(self.list_view)

        self.set_label()
        self.set_model()
        self.set_delegate()

    def set_label(self):
        self.entity_label.setText(self.text)

    def set_model(self):
        if self.model_data:
            self.model = DetailModel(self.model_data)
        else:
            self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

    def set_delegate(self):
        delegate = TaskDelegate(self)
        self.list_view.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        for i in xrange(self.model.rowCount()):
            self.list_view.openPersistentEditor(self.model.index(i, 0))

    def close_delegate(self):
        for i in xrange(self.model.rowCount()):
            self.list_view.closePersistentEditor(self.model.index(i, 0))


class DetailModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(DetailModel, self).__init__(parent)
        self.__model_data = model_data

    @property
    def model_data(self):
        return self.__model_data

    @model_data.setter
    def model_data(self, value):
        self.__model_data = value

    def rowCount(self, parent=QModelIndex()):
        return len(self.__model_data)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return
        row = index.row()
        if role == Qt.DisplayRole:
            return self.__model_data[row]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class TaskDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        cell_widget = CellTaskWidget(parent)
        return cell_widget

    def setEditorData(self, editor, index):
        item = index.model().data(index, Qt.DisplayRole)
        if item:
            editor.set_image(item.pix_map)
            info = "%s - %s" % (item.step, item.task)
            editor.set_info(info)

    def sizeHint(self, option, index):
        return QSize(300, 90)


class CellTaskWidget(QWidget):
    def __init__(self, parent=None):
        super(CellTaskWidget, self).__init__(parent)
        main_layout = QHBoxLayout(self)
        # self.setAutoFillBackground(True)
        self.thumb_label = QLabel()
        self.info_label = QLabel()
        self.actions_btn = QPushButton("Actions")
        main_layout.addWidget(self.thumb_label)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.actions_btn)
        main_layout.setStretch(0, 3)
        main_layout.setStretch(1, 10)
        main_layout.setStretch(2, 1)
        main_layout.setStretchFactor(self.thumb_label, 0)
        main_layout.setStretchFactor(self.info_label, 1)
        main_layout.setStretchFactor(self.actions_btn, 0)
        # palette = QPalette()
        # palette.setColor(QPalette.Background, QColor("#ff0000"))
        # self.setPalette(palette)

    def set_image(self, pix_map):
        self.thumb_label.setPixmap(pix_map)

    def set_info(self, info):
        self.info_label.setText(info)

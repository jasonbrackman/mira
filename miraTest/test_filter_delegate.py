from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *



class GpuModel(QAbstractTableModel):
    def __init__(self, arg=[], headers=[], parent=None):
        super(GpuModel, self).__init__(parent)
        self.arg = arg
        self.headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self.arg)

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            return self.arg[row][column]

    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.arg[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]


class ComboDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ComboDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 1:
            combo = QComboBox(parent)
            combo.addItems(["mdl", "shd"])
            combo.currentIndexChanged.connect(self.onCurrentIndexChanged)
            return combo

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        source_index = model.mapToSource(index)
        model.sourceModel().setData(source_index, value, Qt.DisplayRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def onCurrentIndexChanged(self, index):
        self.commitData.emit(self.sender())
        
        
class GpuToMdlUI(QDialog):
    def __init__(self, parent=None):
        super(GpuToMdlUI, self).__init__(parent)
        self.resize(400, 300)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 1, 0, 1)
        # filter layout
        filter_layout = QHBoxLayout()
        filter_layout.addStretch()
        self.filter_le = QLineEdit()
        filter_layout.addWidget(self.filter_le)
        # table view
        self.table_view = QTableView()
        # button layout
        button_layout = QHBoxLayout()
        self.print_btn = QPushButton("print")
        button_layout.addStretch()
        button_layout.addWidget(self.print_btn)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(button_layout)
        
        self.print_btn.clicked.connect(self.do_print)
        
        self.set_model()
        self.set_delegate()
    
    def set_model(self):
        self.table_view.setSortingEnabled(True)
        self.table_view.verticalHeader().hide()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(0)
        self.table_view.setModel(self.proxy_model)
        headers = ["name", "mdl/shd"]
        model_data = [["heshuai", "mdl"], ["zhaopeng", "mdl"], ["xiedonghang", "mdl"]]
        self.data_model = GpuModel(model_data, headers)
        self.proxy_model.setSourceModel(self.data_model)
        self.table_view.resizeColumnToContents(0)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.filter_le.textChanged.connect(self.set_filter)
        column_width_list = [200, 100]
        for column in range(2):
            self.table_view.setColumnWidth(column, column_width_list[column])

    def set_delegate(self):
        delegate = ComboDelegate(self)
        self.table_view.setItemDelegateForColumn(1, delegate)
        for i in xrange(self.proxy_model.rowCount()):
            self.table_view.openPersistentEditor(self.proxy_model.index(i, 1))
            
    def set_filter(self, value):
        self.proxy_model.setFilterRegExp(value)
        self.set_delegate()
        
    def get_selected(self):
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            return
        selected_rows = list(set([self.proxy_model.mapToSource(i).row() for i in selected_indexes]))
        selected = list()
        for row in selected_rows:
            name = self.data_model.index(row, 0).data()
            mdl_or_shd = self.data_model.index(row, 1).data()
            selected.append([name, mdl_or_shd])
        return selected
        
    def do_print(self):
        selected = self.get_selected()
        print selected[0]
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    hh = GpuToMdlUI()
    hh.show()
    app.exec_()

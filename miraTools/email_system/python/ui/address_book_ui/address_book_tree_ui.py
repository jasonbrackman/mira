# -*- coding: utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from . import address_book_model
from ...libs import get_conf_data


def get_user_data():
    user_data = get_conf_data.get_conf_data("user")
    return user_data


class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self.children = list()
        self._parent = parent
        if parent:
            parent.addChild(self)

    def addChild(self, child):
        self.children.append(child)

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent.children.index(self)

    def isValid(self):
        return False


class GroupNode(Node):
    def __init__(self, name, parent=None):
        super(GroupNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "group"


class UserNode(Node):
    def __init__(self, name, parent=None):
        super(UserNode, self).__init__(name, parent)

    @property
    def node_type(self):
        return "user"


class AddressBookTreeView(QTreeView):
    def __init__(self, parent=None):
        super(AddressBookTreeView, self).__init__(parent)
        self.user_data_dict = get_user_data()
        self.set_model()
        self.setSortingEnabled(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def set_model(self):
        self.root_node = Node("address")
        for key in self.user_data_dict:
            group_name = key
            users = self.user_data_dict[key]
            group_node = GroupNode(group_name, self.root_node)
            for user in users:
                user_node = UserNode(user, group_node)

        self.data_model = address_book_model.AddressBookModel(self.root_node, self)
        self.proxy_model = address_book_model.LeafFilterProxyModel()
        self.proxy_model.setSourceModel(self.data_model)
        self.setModel(self.proxy_model)
        self.resizeColumnToContents(0)


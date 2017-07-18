#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur|http://wingedwhitetiger.com/'


class AssetObject(object):
    def __init__(self, name, workarea, publish, parent=None):
        self.name = name
        self.workarea = workarea
        self.publish = publish
        self.children = []
        self.parent = parent

        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def child(self, row):
        return self.children[row]

    def count(self):
        return len(self.children)

    def row(self):
        if self.parent is not None:
            return self.parent.children.index(self)

    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += '\t'

        output += self.name + '\n'

        for child in self.children:
            output += child.log(tabLevel)

        tabLevel -= 1

        return output

    def __repr__(self):
        return self.log()


if __name__ == "__main__":
    pass


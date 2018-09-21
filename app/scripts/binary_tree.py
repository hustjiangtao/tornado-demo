# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""
simple demo for binary tree
reference:
    https://github.com/qiwsir/algorithm/blob/master/binary_tree.md
    https://github.com/julycoding/The-Art-Of-Programming-By-July/blob/master/ebook/zh/03.01.md
    https://www.jianshu.com/p/e86bc2c0d51c
    https://segmentfault.com/a/1190000013766957
"""


class Node(object):
    """
    def a node obj
    """

    def __init__(self, data):
        """init a root node"""
        self.left = None
        self.data = data
        self.right = None

    def print_tree(self):
        """print this tree"""
        if self.left is not None:
            self.left.print_tree()
        print(self.data)
        if self.right is not None:
            self.right.print_tree()

    def insert(self, data):
        """insert a new sub node"""
        if data < self.data:
            if self.left is None:
                self.left = Node(data)
            else:
                self.left.insert(data)
        elif data > self.data:
            if self.right is None:
                self.right = Node(data)
            else:
                self.right.insert(data)

    def lookup(self, data, parent=None):
        """lookup the given data in the tree with (node, parent)"""
        if data < self.data:
            if self.left is None:
                return None, None
            else:
                return self.left.lookup(data, self)
        elif data > self.data:
            if self.right is None:
                return None, None
            else:
                return self.right.lookup(data, self)
        else:
            return self, parent

    def delete(self, data):
        """delete a given node"""
        pass

    def compare_tree(self, node):
        """compare the given tree with self tree"""
        pass

    def children_count(self):
        """count the children node"""
        pass

    def tree_data(self):
        """generator for tree data"""
        pass


node = Node

if __name__ == '__main__':
    root = node(7)
    root.insert(3)
    root.insert(1)
    from random import randint
    # print(randint(1, 100))
    for i in range(20):
        root.insert(randint(1, 100))
    root.print_tree()
    print(root.lookup(8))

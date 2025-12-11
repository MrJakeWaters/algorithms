import random
import uuid
import math


class Node:
    def __init__(self, values=None, max_value_size=4):
        # set base attributes
        self.id = uuid.uuid4()
        '''
        # if the node has a parent and it's inside the leaf_nodes array, this is the index of the node (or position)
        # this is used to understand where to insert a value when you are outside the scope of a Node
        '''
        self.leaf_index = 0 
        self.values = []
        self.max_value_size = max_value_size
        self.min_value_size = math.floor(self.max_value_size/2)
        self.leaf_nodes = []
        self.next = None
        self.previous = None

        # add value if required
        if values is not None and len(values) > 0:
            for x in values:
                self.add(x)


    def reindex(self):
        # update node indices
        for i, x in enumerate(self.leaf_nodes):
            x.leaf_index = i

    
    def add_leaf_node(self, node):
        # adds a node to the correct position in the self.leaf_nodes array
        # leaf_index is the position this node is inside of another Nodes .leaf_nodes array
        # insert value one greater
        self.leaf_nodes.insert(node.leaf_index+1, node)
        for i,x in enumerate(self.leaf_nodes[node.leaf_index:]):
            x.leaf_index = i


    def traverse(self, value):
        # recursive searches to find the node, inside the nested nodes, where the value should be inserted
        node = self
        while len(node.leaf_nodes) != 0:
            node.leaf_nodes[self.get_insert_index(value)].previous = node # set the previous value to be able to traverse back
            node.next = node.leaf_nodes[self.get_insert_index(value)] # set next to the indexed node
            node = node.next
        return node


    def get_insert_index(self, value):
        # return the index where the value should be inserted so that self.values
        # is in ascending order
        l = len(self.values)
        if l == 0:
            return 0

        else:
            # x is the index, which must start at 1 with 0 being edge case that is handle above
            # ex. range(5) = [0,1,2,3,4]
            for x in range(l):
                i = l-x-1
                insert_index = 0

                if value >= self.values[i]:
                    insert_index = i+1
                    break

            return insert_index

    # add value in sorted order
    def add(self, value):
        self.values.insert(self.get_insert_index(value), value)


    def split(self):
        # set split values
        split_index = math.floor(len(self.values)/2)
        center = [self.values[split_index]]
        left = self.values[:split_index]
        right = self.values[split_index+1:]

        # update current node values
        self.values = left

        # return values that will go to leaf_nodes or parent node
        return center, right
        

class Btree:
    def __init__(self, node=Node()):
        self.node = node


    def display(self, level, node):
        # print values
        print('[%s, %s] %s> %s' % (node.leaf_index, node.id, '-'*level, ','.join([str(x) for x in node.values])))

        # recursive call of each node
        for leaf_node in node.leaf_nodes:
            self.display(level+1, leaf_node)


    def insert(self, value):
        # traverse to the bottom of the tree and add the value
        insert_node = self.node.traverse(value)
        insert_node.add(value)

        # split the node if there are too many values
        while len(insert_node.values) > insert_node.max_value_size:
            add_value, leaf_node_values = insert_node.split()

            # check if the parent node is empty and create if it doesn't exists
            # otherwise traverse back up the tree splitting where necessary
            if insert_node.previous is None:
                # create a parent node
                insert_node.previous = Node(add_value)

                # set to the parent node and update it's leaf nodes
                self.node = insert_node.previous
                for i, x in enumerate([insert_node, Node(leaf_node_values)]):
                    self.node.add_leaf_node(x)

            else:
                insert_node.previous.add(add_value[0]) # add value
                insert_node.previous.add_leaf_node(Node(leaf_node_values)) # add leaf node
                insert_node = insert_node.previous

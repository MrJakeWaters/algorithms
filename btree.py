import random
import uuid
import math


class SplitNode:
    def __init__(self, left, right, center):
        self.current_values = left
        self.leaf_node_values = right
        self.parent_value = center


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
        self.child = None
        self.parent = None

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
            node.leaf_nodes[self.get_insert_index(value)].parent = node # set the.parent value to be able to traverse back
            node.child = node.leaf_nodes[self.get_insert_index(value)] # set.child to the indexed node
            node = node.child
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
        center = self.values[split_index]
        left = self.values[:split_index]
        right = self.values[split_index+1:]

        # return values that will go to leaf_nodes or parent node
        return SplitNode(left, right, center)
        

class Btree:
    def __init__(self, node=Node()):
        self.node = node


    def get_level_min(self, level):
        # get min value for a particular level within the tree
        node = self.node

        if len(node.leaf_nodes) > 0:
            for x in range(level):
                node = node.leaf_nodes[0]

        # get the smallest value (b/c it's sorted this is the first value)
        return node.values[0]


    def display(self, level, node):
        # print values
        print('[%s, %s] %s> %s' % (node.leaf_index, node.id, '----'*level, ','.join([str(x) for x in node.values])))

        # recursive call of each node
        for leaf_node in node.leaf_nodes:
            self.display(level+1, leaf_node)


    def insert(self, value):
        # traverse to the bottom of the tree and add the value
        current_node = self.node.traverse(value)
        current_node.add(value)

        # split the node if there are too many values
        while len(current_node.values) > current_node.max_value_size:
            split_node = current_node.split() # this returns SplitNode object storing parent_value, leaf_node_values and current_values

            # check if the parent node is empty and create if it doesn't exists
            # otherwise traverse back up the tree splitting where necessary
            if current_node.parent is None:
                # create a parent node
                current_node.parent = Node([split_node.parent_value])

                # update leaf nodes of newly created parent
                current_node.parent.add_leaf_node(current_node) # move current node to the leaf nodes in the parent

                # make btree node equal to the newly created parent
                self.node = current_node.parent
            else:
                current_node.parent.add(split_node.parent_value)

            # create new leaf node and add it to parent leaves
            new_leaf_node = Node(split_node.leaf_node_values)
            current_node.parent.add_leaf_node(new_leaf_node)

            # update parent node with split value
            current_node.values = split_node.current_values # updating current node (this removes the last math.floor(self.max_value_size/2)+1 values from the array)

            # if there are nested leaf nodes within the current_node they need to be properly
            # separated so the current_node takes only half and newly added node take the other half
            if len(current_node.leaf_nodes) > 0:
                leaf_node_split_index = len(current_node.parent.values) + 1 # index that splits the leaf node array to what's going to new_node
                new_leaf_node.leaf_nodes = current_node.leaf_nodes[:leaf_node_split_index]
                current_node.leaf_nodes = current_node.leaf_nodes[leaf_node_split_index:] # move last x values to new_node 

                # reindex each updated nodes
                new_leaf_node.reindex()
                current_node.reindex()

            # update current_node for loop
            current_node = current_node.parent

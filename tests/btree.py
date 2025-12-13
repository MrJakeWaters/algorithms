import unittest
import random
from btree import Node, Btree


class BtreeUnitTests(unittest.TestCase):
    def testAddValueToNodeInSortedOrder(self):
        # create random values and add them to the node list
        # ensuring they end up in sorted order
        base = [random.randint(-1000,1000) for x in range(10)]

        # create node and insert base values
        node = Node(base[:5], 10)

        # use add function to insert the rest
        for x in base[5:]:
            node.add(x)

        # validate
        self.assertEqual(sorted(base), node.values)

    def valuesDoNotExceedMaxLengthRecursive(self, node):
        message = '\t[%s, %s] # of Values:%s, Max Size: %s' % (node.leaf_index, node.id, str(len(node.values)), str(node.max_value_size))
        if len(node.leaf_nodes) > 0:
            for x in node.leaf_nodes:
                self.valuesDoNotExceedMaxLengthRecursive(x)
        else:
            self.assertLessEqual(len(node.values), node.max_value_size, msg=message)


    def testValuesDoNotExceedMaxLength(self):
        # create random values with a list that is 1 value greater than node size
        # and test that none of the nodes have more than the node default size
        # default max_values_size = 4, this means once a 5th value is added a split should be performed
        base = [random.randint(-1000,1000) for x in range(15)]
        
        # create node and add 
        btree = Btree()
        for x in base:
            btree.insert(x)
        
        # recursively check that each node doesn't exceed max length
        self.valuesDoNotExceedMaxLengthRecursive(btree.node)


    def correctNumberOfLeafNodesRecursive(self, node):
        # should have one more leaf node than the number of values
        message = '\t[%s, %s] # of Values:%s, # of Leaf Nodes: %s' % (node.leaf_index, node.id, str(len(node.values)), str(len(node.leaf_nodes)))
        if len(node.leaf_nodes) > 0:
            self.assertEqual(len(node.values)+1, len(node.leaf_nodes))
            for x in node.leaf_nodes:
                self.correctNumberOfLeafNodesRecursive(x)


    def testHasCorrectNumberOfLeafNodesDepth3(self):
        # create random values with a list that is 1 value greater than node size
        # and test that none of the nodes have more than the node default size
        # default max_values_size = 4, this means once a 5th value is added a split should be performed
        base = [random.randint(-1000,1000) for x in range(5)]
        
        # create node and insert base values
        # this will create a depth of 2
        btree = Btree()
        for x in base:
            btree.insert(x)

        # add enough specific values so that one node will split again
        for x in list(range(12)):
            random_node_min = btree.get_level_min(1) - random.randint(0, 100) # ensure the random value is lower than the current min
            btree.insert(random_node_min)

        # recursively check that each node doesn't exceed max length
        print('\n') # added for formatting purposes only when printing out node results from valueDoNotExceedMaxLengthRecursive
        try:
            self.correctNumberOfLeafNodesRecursive(btree.node)
        except Exception as e:
            btree.display(1, btree.node)
            self.assertEqual(1,0)


    def testHasCorrectNumberOfLeafNodesDepth2(self):
        # create random values with a list that is 1 value greater than node size
        # and test that none of the nodes have more than the node default size
        # default max_values_size = 4, this means once a 5th value is added a split should be performed
        base = [random.randint(-1000,1000) for x in range(5)]
        
        # create node and insert base values
        # this will create a depth of 2
        btree = Btree()
        for x in base:
            btree.insert(x)

        # recursively check that each node doesn't exceed max length
        print('\n') # added for formatting purposes only when printing out node results from valueDoNotExceedMaxLengthRecursive
        btree.display(1, btree.node)
        try:
            self.correctNumberOfLeafNodesRecursive(btree.node)
        except Exception as e:
            btree.display(1, btree.node)
            self.assertEqual(1,0)


if __name__ == '__main__':
    unittest.main()

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0

    # assistant functions for the required ones

    """Returns the minimal node in the subtree whose root is self.
		@return:
	"""

    def subtree_minimum(self):
        node = self
        while node.left.key is not None:
            node = node.left
        return node

    # Time complexity - O(logn) (n is the number of nodes in the tree, the biggest subtree is the whole tree).

    """
	Returns the successor of self.
	"""

    def successor(self):
        if self.right.key is not None:
            return self.right.subtree_minimum()
        else:
            parent = self.parent
            node = self
            while parent is not None and node == parent.right:
                node = parent
                parent = node.parent
            return parent

    # Time complexity - O(logn) (n is the number of nodes in the tree).

    """returns the height
	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""

    def get_height(self):
        return self.height

    # Time complexity - O(1)

    """sets the height of the node
	@type h: int
	@param h: the height
	"""

    def set_height(self, h):
        self.height = h

    # Time complexity - O(1)

    """returns whether self is not a virtual node
	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def is_real_node(self):
        if self.key is None:
            return False
        return True

    # Time complexity - O(1)

    """
	Function that computes the height of the given node
	@return: The height of the node.
	"""

    def compute_height(self):
        return max(self.left.height, self.right.height) + 1

    # Time complexity - O(1).

    """
	Function that computes the BF of the given node
	Time complexity - O(1).
	@return: The BF of the node.
	"""

    def compute_BF(self):
        return self.left.height - self.right.height


# Time complexity - O(1).

"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
	Constructor, you are allowed to add more fields.  

	"""

    def __init__(self):
        self.root = None

    """searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""

    def search(self, key):
        if self.root is None:
            return None

        def search_rec(node, my_key):
            if node.key == my_key:
                return node
            if not node.is_real_node():
                return None
            if node.key < my_key:
                return search_rec(node.right, my_key)
            else:
                return search_rec(node.left, my_key)

        return search_rec(self.root, key)

    # O(log n) time complexity (n is the number of nodes in the tree).

    # insert & delete assistant functions:

    """
	Function that performs the left rotation.
	"""

    def left_rotation(self, node):
        prev_right = node.right
        prev_parent = node.parent

        node.right = prev_right.left
        node.right.parent = node
        prev_right.left = node
        # Change B's prev_parent to be A's parent
        prev_right.parent = prev_parent
        if prev_parent is not None:
            if prev_parent.left == node:
                prev_right.parent.left = prev_right
            else:
                prev_right.parent.right = prev_right
        node.parent = prev_right
        # Set heights and sizes of A and B
        node.size = node.left.size + node.right.size + 1
        prev_right.size = prev_right.left.size + prev_right.right.size + 1
        node.height = node.compute_height()
        prev_right.height = prev_right.compute_height()

        if node == self.root:
            self.root = prev_right

    #  O(1) time complexity

    """
	Function that performs the right rotation.
	"""

    def right_rotation(self, node):
        prev_left = node.left
        prev_parent = node.parent

        node.left = prev_left.right
        node.left.parent = node
        prev_left.right = node
        prev_left.parent = prev_parent
        if prev_parent is not None:
            if prev_parent.left == node:
                prev_left.parent.left = prev_left
            else:
                prev_left.parent.right = prev_left
        node.parent = prev_left
        # Set heights and sizes of A and B
        node.size = node.left.size + node.right.size + 1
        prev_left.size = prev_left.left.size + prev_left.right.size + 1
        node.height = node.compute_height()
        prev_left.height = prev_left.compute_height()

        if node == self.root:
            self.root = prev_left

    #  O(1) time complexity

    """
	Updating height and size fields after insertion or deletion of a node.
	Applying the suitable rotation, if needed.
	"""

    def rebalancing_upwards(self, node, size):
        balance_counter = 0
        while node is not None:
            current_height = node.get_height()
            new_height = node.compute_height()
            node_BF = node.compute_BF()
            if abs(node_BF) < 2:
                if new_height != current_height:
                    # The height changed
                    node.set_height(new_height)
                    balance_counter += 1
                node.size += size
                node = node.parent
            else:
                if node_BF == 2:
                    left_son = node.left
                    # left then right rotation
                    if left_son.compute_BF() == -1:
                        self.left_rotation(left_son)
                        self.right_rotation(node)
                        balance_counter += 2
                    else:
                        self.right_rotation(node)
                        balance_counter += 1
                else:
                    right_son = node.right
                    if right_son.compute_BF() == 1:
                        self.right_rotation(right_son)
                        self.left_rotation(node)
                        balance_counter += 2
                    else:
                        self.left_rotation(node)
                        balance_counter += 1
                node = node.parent.parent

        return balance_counter

    # O(log n) time complexity (n is the number of nodes in the tree).

    """inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def insert(self, key, val):
        node = self.root
        if node is None:
            node = AVLNode(key, val)
            self.root = node
        else:
            while node.key is not None:
                if key < node.key:
                    node = node.left
                else:
                    node = node.right
            node.key = key
            node.value = val

        node.height = 0
        node.size = 1
        # Setting virtual children
        node.left = AVLNode(None, None)
        node.left.parent = node
        node.right = AVLNode(None, None)
        node.right.parent = node

        # Fixing and updating heights and sizes after insertion
        node = node.parent
        return self.rebalancing_upwards(node, size=1)

    # O(log n) time complexity (n is the number of nodes in the tree).

    """deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def delete(self, node):
        parent = node.parent
        if not node.left.is_real_node() and not node.right.is_real_node():
            node.key = None
            node.value = None
            node.height = -1
            node.left = None
            node.right = None
            node.size = 0

        # Case 2 - has only one child
        # has right child
        elif not node.left.is_real_node():
            # node is root
            if node.parent is None:
                node.right.parent = None
                self.root = node.right
            # regular node
            else:
                node.right.parent = node.parent
                # Checking if node is the right/left son of parent
                if node.parent.right == node:
                    node.parent.right = node.right
                else:
                    node.parent.left = node.right

        # has left child
        elif not node.right.is_real_node():
            # node is root
            if node.parent is None:
                node.left.parent = None
                self.root = node.left
            # regular node
            else:
                node.left.parent = node.parent
                # Checking if node is the right/left son of parent
                if node.parent.right == node:
                    node.parent.right = node.left
                else:
                    node.parent.left = node.left

        # Case 3 - the current node has two children
        else:
            successor = node.successor()
            successor_key = successor.key
            successor_value = successor.value
            parent = successor.parent
            balance_counter = self.delete(successor)
            node.key = successor_key
            node.value = successor_value
            return balance_counter

        # Fixing and updating heights after insertion
        return self.rebalancing_upwards(parent, size=-1)

    # O(log n) time complexity (n is the number of nodes in the tree).

    """returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self):

        def avl_to_array_rec(node):
            if node is None or node.key is None:
                return []
            left_side = avl_to_array_rec(node.left)
            right_side = avl_to_array_rec(node.right)
            return left_side + [(node.key, node.value)] + right_side

        return avl_to_array_rec(self.root)
        # goes recursively over the tree

    # O(n) time complexity

    """returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        if self.root is None:
            return 0

        return self.root.size

    # O(1) time complexity

    """compute the rank of node in the dictionary

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary to compute the rank for
	@rtype: int
	@returns: the rank of node in self
	"""

    def rank(self, node):
        rank_counter = node.left.size + 1
        parent = node.parent
        while parent is not None:
            if parent.key < node.key:
                rank_counter += parent.left.size + 1
            parent = parent.parent
        return rank_counter

    # O(log n) time complexity

    """finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	"""

    def select(self, i):
        node = self.root
        while node.key is not None:
            left_subtree = node.left.size + 1
            if left_subtree == i:
                return node
            elif left_subtree > i:
                node = node.left
            else:
                i -= left_subtree
                node = node.right

    # O(log n) time complexity

    """finds the node with the largest value in a specified range of keys

	@type a: int
	@param a: the lower end of the range
	@type b: int
	@param b: the upper end of the range
	@pre: a<b
	@rtype: AVLNode
	@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
	"""

    def max_range(self, a, b):
        if self.root is None:
            return None

        def candidate_rec(node, arg1, arg2):
            if node.key is None or not a <= node.key <= b:
                return []
            left_child = candidate_rec(node.left, a, b)
            right_child = candidate_rec(node.right, a, b)
            return left_child + [node] + right_child
        # creates an array of nodes whose keys are in [a,b]

        def max_value(list_of_nodes):
            if len(list_of_nodes) == 0:
                return None

            max_v = list_of_nodes[0]
            for node in list_of_nodes:
                if node.value > max_v.value:
                    max_v = node
            return max_v
        # finds the node in said array that has the biggest value

        candidate_list = candidate_rec(self.root, a, b)
        return max_value(candidate_list)

    # O(n) time complexity

    """returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        return self.root

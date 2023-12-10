import math


class Node():
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.parent = self.child = None
        self.left = self.right = self
        self.degree = 0
        self.flag = False


class FibonacciHeap():
    def __init__(self):
        self.min = None
        self.no_nodes = 0

    def get_min(self):
        '''
        Returns minimum Node
        Сomplexity: O(1)
        '''

        return self.min

    def insert(self, key, value=None):
        '''
        Insert new value into the heap
        Complexety: O(1)
        '''

        if value is None:
            value = key
        n = Node(key, value)

        if self.no_nodes == 0:
            self.min = n
        else:
            self.add_root(n)

        self.no_nodes += 1

        return n

    def delete(self, node):
        '''
        Removes node from the heap
        Complexety: O(log(n))
        '''

        self.decrease_key(node, self.min.key - 1)
        self.delete_min()

    def delete_min(self):
        '''
        Removes minimum node from the heap
        Complexety: O(log(n))
        '''

        prev_min = self.min
        if prev_min is not None:

            # move children to root
            if prev_min.child is not None:
                n = stop = prev_min.child
                first_loop = True
                while first_loop or n != stop:
                    first_loop = False
                    next_node = n.right
                    self.add_node_left(n, self.min)
                    n.parent = None
                    n = next_node

            if self.min.right != self.min:
                self.min = prev_min.right
                self.remove_node(prev_min)
                self.consolidate()
            # no nodes left
            else:

                start_for_newmin = prev_min.right
                self.remove_node(prev_min)
                self.find_new_min(start_for_newmin)

            self.no_nodes -= 1
        return prev_min

    def find_new_min(self, start_for_newmin):
        '''Finds new minimum in heap after previous was deleted'''

        node = stop = start_for_newmin
        flag = False
        min_value = float('inf')
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            if node.key < min_value:
                self.min = node
                min_value = node.key
            node = node.right

    def consolidate(self):
        '''Make the degrees of root elements unique, fibonacci sequence'''

        degree_arr = [None for _ in range(int(math.log(self.no_nodes, 2)) + 2)]
        root_items = self.layer_as_list(self.min)
        for n in root_items:

            degree = n.degree
            # combine nodes until no same root degrees exists
            while degree_arr[degree] is not None:
                m = degree_arr[degree]
                # make sure that n is always smaller
                if m.key < n.key:
                    n, m = self.swap_vars(n, m)
                self.remove_node(m)
                self.add_child(m, n)
                degree_arr[degree] = None
                degree += 1

            degree_arr[degree] = n

        self.update_root_min()

    def update_root_min(self):
        '''Update self.min to lowest value from the root'''

        top = self.find_root_item()
        root_layer = self.layer_as_list(top)
        self.min = min(root_layer, key=lambda n: n.key)

    def find_root_item(self):
        '''Return an item from root layer'''

        top_item = self.min
        while top_item.parent is not None:
            top_item = top_item.parent
        return top_item

    def decrease_key(self, node, new_key):
        '''Changes key for node'''

        node.key = new_key
        parent = node.parent

        if parent is None:
            if node.key < self.min.key:
                self.min = node
        elif node.key < parent.key:
            self.cut(node)
            self.cascading_cut(parent)

        return node

    def cut(self, node):
        '''Move the node root level'''

        parent = node.parent
        parent.degree -= 1

        if parent.child == node and node.right == node:
            parent.child = None
            self.remove_node(node)
        else:
            parent.child = node.right
            self.remove_node(node)

        node.flag = False
        self.add_node_left(node, self.min)
        if node.key < self.min.key:
            self.min = node

    def cascading_cut(self, node):
        parent = node.parent
        if parent is not None:
            if parent.flag:
                self.cut(node)
                self.cascading_cut(parent)
            else:
                parent.flag = True

    def merge(self, heap):
        '''
        Merge two heaps
        Complexety: O(log(n))
        '''

        assert isinstance(heap, FibonacciHeap)

        if heap.min is None:
            return
        if self.min is None:
            self.min = heap.min
            return

        first = self.min
        last = self.min.right
        second = heap.min
        second_last = heap.min.left

        first.right = second
        second.left = first
        last.left = second_last
        second_last.right = last

        self.no_nodes += heap.no_nodes
        if heap.min.key < self.min.key:
            self.min = heap.min

    def add_node_left(self, node, right_node):
        '''Add node to left side of the given right_node'''

        node.right = right_node
        node.left = right_node.left
        right_node.left.right = node
        right_node.left = node

    def add_root(self, node):
        '''Add node to left side of the given right_node'''

        self.add_node_left(node, self.min)
        if node.key < self.min.key:
            self.min = node

    def add_child(self, child, parent):
        '''Add node as child to another node'''

        if parent.child is None:
            parent.child = child
            child.parent = parent
        else:
            self.add_node_left(child, parent.child)
            child.parent = parent
        parent.degree += 1

    def swap_vars(self, var1, var2):
        '''Swap variables'''

        return (var2, var1)

    def remove_node(self, node):
        '''Remove element from the double linked list'''

        node.left.right = node.right
        node.right.left = node.left
        node.left = node
        node.right = node
        node.parent = None

    def layer_as_list(self, node):
        '''
        Return the whole layer as a list.
        One node from the layer must be given
        '''

        items = []
        n = stop = node
        first_loop = True
        while first_loop or n != stop:
            first_loop = False
            items.append(n)
            n = n.right
        return items

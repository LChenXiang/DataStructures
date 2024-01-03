"""
Ukkonen's Suffix Tree implementation
"""

from operator import attrgetter

leaf_end = -1
A = ord('A')

class Node:

    def __init__(self, is_leaf, size=27):
        self.children = [None] * size
        self.is_leaf = is_leaf
        self.start = None
        self.end = None
        self.suff_idx = None
        self.suff_link = None
        
    def edge_length(self):
        return self.end - self.start + 1

    def __eq__(self, node):
        atr = attrgetter('start', 'end', 'suff_idx')
        return atr(self) == atr(node)

    def __ne__(self, node):
        atr = attrgetter('start', 'end', 'suff_idx')
        return atr(self) != atr(node)

    def __str__(self):
        print(self.children)
        print(self.start)
        print(self.end)
        print(self.is_leaf)
        print(self.suff_idx)
        print(self.suff_link)
        return ""

class SuffixTree:

    def __init__(self, s):
        self.s = s

        self.latest_node = None

        self.active_node = None        
        self.active_edge = -1
        self.active_length = 0

        self.remaining_suff = 0

        self.root = None
        self.root_end = None

        self.split_end = None

        self.size = 0
    
    def create_node(self, start, end=None, is_leaf=False):
        node = Node(is_leaf)
        
        node.start = start
        
        if is_leaf:
            node.end = leaf_end        
        else:
            node.end = end

        node.suff_link = self.root
        node.suff_idx = -1

        return node

    """
    TRICK 1: Skip/Count
    """
    def walked_down(self, node):
        # print("TRICK 1: Skip/Count")
        walked_down = False
        length = node.edge_length()

        if self.active_length >= length:
            self.active_edge += length
            self.active_length -= length
            self.active_node = node
            walked_down = True

        return walked_down
        
    def extend(self, i):
        # print("RULE 1: Once a leaf, always a leaf") 
        global leaf_end
        leaf_end = i

        self.remaining_suff += 1

        self.latest_node = None

        while(self.remaining_suff > 0):
            if self.active_length == 0:
                self.active_edge = ord(self.s[i]) - A
                

            # active_edge_idx = ord(self.s[i]) - A
            # print(f"active edge idx: {self.active_edge}")
            # print(self.active_node)
            if self.active_node.children[self.active_edge] is None:
                # print("RULE 2: Make a new leaf")
                child = self.create_node(i, is_leaf=True)
                self.active_node.children[self.active_edge] = child

                if self.latest_node is not None:
                    self.latest_node.suff_link = self.active_node
                    self.latest_node = None
            
            else:
                next_node = self.active_node.children[self.active_edge]
                if self.walked_down(next_node):
                    continue
                
                chr_active_edge_idx = next_node.start + self.active_length
                if self.s[chr_active_edge_idx] == self.s[i]:
                    # print("RULE 3: Showstopper")
                    if self.latest_node is not None and self.active_node != self.root:
                        self.latest_node.suff_link = self.active_node
                        self.latest_node = None
                    
                    self.active_length += 1
                    break
                
                self.split_end = next_node.start + self.active_length - 1
                split_node = self.create_node(next_node.start, self.split_end)

                self.active_node.children[self.active_edge] = split_node

                split_node.children[self.active_edge] = self.create_node(i, is_leaf=True)

                next_node.start += self.active_length
                next_node_idx = self.s[next_node.start - A]
                
                split_node.children[next_node_idx] = next_node

                if self.latest_node is not None:
                    self.latest_node.suff_link = split_node

                self.latest_node = split_node
            
            self.remaining_suff -= 1

            if (self.active_node == self.root) and (self.active_length > 0):
                self.active_length -= 1
                self.active_edge = i - self.remaining_suff + 1

            elif self.active_node != self.root:
                # print(self.active_node)
                self.active_node = self.active_node.suff_link
    
    def build(self):
        self.size = len(self.s)

        self.root_end = -1
        self.root = self.create_node(-1, self.root_end)

        self.active_node = self.root

        for i in range(self.size):
            # print(self.s[i])
            self.extend(i)
        
        self.set_suffix(self.root, 0)

    
    def walk_dfs(self, current):
        
        start, end = current.start, current.end
        # print(f"start: {start}, end: {end}")
        yield self.s[start: end + 1]

        for node in current.children:
            if node is not None:
                yield from self.walk_dfs(node)

    def __str__(self):
        return "\n".join(map(str, self.edges.values()))

    def print_dfs(self):
        for sub in self.walk_dfs(self.root):
            print(sub)

    def set_suffix(self, node, height):
        if node is None:
            return
        
        # if node.start != -1:
        #     print(node.start, node.end)

        leaf = True
        
        for child in node.children:
            if child is not None:
                # if leaf and node.start != -1:
                    # print(f" {node.suff_idx}")

                leaf = False
                self.set_suffix(child, height + child.edge_length())

        if leaf:
            node.suff_idx = self.size - height
            # print(f" {node.suff_idx}")

    def traverse(self, node):
        if node is None:
            return

        if node.suff_idx == -1:
            for child in node.children:
                if child is not None:
                    # print(node.suff_idx)
                    self.traverse(child)

        elif node.suff_idx > -1 and node.suff_idx < self.size:
            print(f" {node.suff_idx}")

    def print_suff(self):
        self.traverse(self.root)

if __name__ == '__main__':
    t = SuffixTree('mississippi$')
    print(t)
    # t.print_dfs()

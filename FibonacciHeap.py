class Heap:
    def __init__(self, key) -> None:
        self.root = Node(key)
        self.h_min = self.root
        self.nodes = 1

    def get_min(self):
        return self.h_min.get_key()

    def merge(self, H2):
        self.h_min.left.right = H2.h_min.right
        H2.h_min.right.left = self.h_min.left
        H2.h_min.right = self.h_min
        self.h_min.left = H2.h_min

        if H2.get_min() < self.get_min():
            self.h_min = H2.h_min

    def insert(self, key, payload=None):
        H2 = Heap(key)
        self.merge(H2)
        self.nodes += 1

    def extract_min(self):
        min_tree = self.h_min
        
        min_tree.left.right = min_tree.right
        min_tree.right.left = min_tree.left

        self.h_min = min_tree.right
        self.nodes -= 1

        if self.nodes == 0:
            self.h_min = None
            return

        

class Node:
    def __init__(self, key, payload=None) -> None:
        self.key = key
        self.payload = payload
        self.degree = 0
        self.left = self
        self.right = self
        self.marked = False
        self.parent = None
        self.child = None
    
    def get_key(self):
        return self.key
        

if __name__ == '__main__':
    H = Heap(1)
    print(H.get_min())
    H.insert(0)
    print(H.h_min.left.get_key())


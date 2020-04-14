from Node import Node
# import Node
class LRU:
    def __init__(self):
        self.head = None
        self.tail = None
        # self.d = {}
        self.l = []

    def get(self):
        '''returns the least recently used to the user'''
        if self.tail is None:
            return None
        elif self.tail.left is None:
            x = self.tail.content
            self.head = None
            self.tail = None
            return x
        else:
            x = self.tail.content
            self.tail = self.tail.left
            self.tail.right = None
            return x



    def put(self, n):
        '''updates the LRU cache based on frequency'''
        if self.head is None:
            self.head = Node(n)
            self.l.append(n)
            self.tail = self.head
            return
        elif n not in self.l:
            self.l.append(n)
            temp = Node(n)
            temp.right = self.head
            self.head.left = temp
            self.head = temp
        else:
            x = self.head
            while x is not None:
                if x.content == n:
                    if x.right is None:
                        self.tail = self.tail.left
                        x.right = self.head
                        self.head.left = x
                        self.head = x
                        self.head.left = None
                        self.tail.right = None
                        break
                    x.left.right = x.right
                    x.right.left = x.left
                    x.right = self.head
                    self.head.left = x
                    self.head = x
                    self.head.left = None
                    break
                x = x.right
            

    def get_cache(self):
        '''returns the entire LRU cache'''
        l = []
        x = self.head
        while x is not None:
            l.append(x.content)
            x = x.right
        return l

def main():
    # test = LRU()
    pass

if __name__ == "__main__":
    main()

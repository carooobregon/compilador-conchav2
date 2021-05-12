class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == [] 
        
    def push(self,item):
        self.items.insert(len(self.items),item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def clear(self):
        self.items = []

    def printQueue(self):
        for i in self.items:
            print(i)
    
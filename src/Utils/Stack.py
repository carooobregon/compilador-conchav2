class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def printStack(self):
        print("mystack")
        c = 0
        for i in self.items:
            print(i, c)
            c+=1

    def clear(self):
        self.items = []
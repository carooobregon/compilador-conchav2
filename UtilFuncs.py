import queue

class UtilFuncs:
    params = []
    def __init__(self):
        self.functionNameQ = queue.Queue()
    
    def addFunctionNameQ(self, f):
        self.functionNameQ.put(f)
        print("q", list(self.functionNameQ.queue))
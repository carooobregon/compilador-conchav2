from queue import Queue

class UtilFuncs:
    q = Queue()

    def __init__(self):
        pass
        # self.functionNameQ = Queue()

    def addFunctionNameQ(self, f):
        self.q.put(f)
        print(list(self.q.queue))
        return 0

    def getLatestFuncNameQ(self):
        if(self.q.empty()):
            return "na"
        else:
            return self.q.get()
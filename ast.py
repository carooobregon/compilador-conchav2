class Termino():
    def evalaokdak(self):
        return 'Programa Valido !'

class Declaracion:
    params = []
    def __init__(self, a):
        self.params = a

    def display(self):
        print("parabb", self.params)
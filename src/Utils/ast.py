class Declaracion:
    params = []
    def __init__(self, a):
        self.params = [a[0].eval(), a[1].value]

    def print(self):
        return 0
        # print("parabb", self.params)

class Termino():
    def eval(self):
        return 'Programa Valido !'

class Tipo:
    params = []
    def __init__(self, a):
        self.params = a

    def eval(self):
        # print("Tipo vals", type(self.params[0].value), self.params[0].value)
        return self.params[0].value
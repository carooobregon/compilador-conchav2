from Utils.UtilFuncs import UtilFuncs

class ParameterHandler:
    listaParams = []
    count = 0
    orderedParms = []
    flatParms = []
    def __init__(self, params, scope, st):
        self.params = params
        self.scope = scope
        self.st = st
        self.util = UtilFuncs()

    def addParamsLista(self):
        self.orderedParms = []
        self.createListParams()
        cont = 0
        while cont < len(self.listaParams)-1:
            self.st.functions[self.scope]["values"][self.listaParams[cont+1].value] = {"tipo": self.listaParams[cont].gettokentype()}
            cont +=3

    def createListParams(self):
        self.st.functions[self.scope]["parms"] = []
        self.getListaParams()
        self.st.functions[self.scope]["parms"] = self.orderedParms

    def getListaParams(self):
        if len(self.params) < 3:
            self.procesSingleParam()
        else:
            self.processManyParams()

    def procesSingleParam(self):
        count = 0
        self.addListaparams()
        self.orderedParms.append(self.util.convertTypes(self.flatparms[0].value))
        count +=3

    def processManyParams(self):
        count = 0
        for i in self.params:
            if isinstance(i, list):
                self.listaParams = self.util.flatten(i)
        self.listaParams.append(',')
        self.addListaparams()
        while(count < len(self.flatparms)):
            self.orderedParms.append(self.util.convertTypes(self.flatparms[count].value))
            count +=3 

    def addListaparams(self):
        self.listaParams.append(self.params[0])
        self.listaParams.append(self.params[1])
        self.flatparms = self.util.flatten(self.params)
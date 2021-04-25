class SemanticCube:
    def __init__(self):
        print()

    def validateType(self,leftOp, operacion, rightOp):
        if (leftOp == "CONSTANTE_ENT" and rightOp =="CONSTANTE_ENT") :
            print("int")
        elif (leftOp == "CONSTANTE_ENT" and  rightOp =="CONSTANTE_FLOT") or (leftOp == "CONSTANTE_FLOT" and rightOp =="CONSTANTE_ENT") :
            print("float")
        elif (leftOp == "CONSTANTE_FLOT" and  rightOp =="CONSTANTE_FLOT")  :
            print("float")


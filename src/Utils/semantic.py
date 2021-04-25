class SemanticCube:
    def __init__(self):
        print()

    def validateType(self,leftOp, rightOp):
        if (leftOp == "INT" and rightOp =="CTE_ENT") or (leftOp == "INT" and rightOp == "INT"):
            print("CTE_ENT")
            return True
        elif (leftOp == "INT" and rightOp =="CTE_FLOAT") or (leftOp == "INT" and rightOp =="FLOT") :
            print("float") 
            return True
        elif (leftOp == "STRING" and rightOp == "STRING") or (leftOp == "STRING" and rightOp == "STR") or (leftOp == "STR" and rightOp == "STRING"):
            print("string")
            return True
        elif (leftOp == "STRING" and rightOp == "INT") or (leftOp == "STRING" and rightOp == "CTE_ENT") or (leftOp == "STRING" and rightOp == "FLOT") or (leftOp == "STRING" and rightOp == "CTE_FLOT"):
            print("error")
            return True 
        elif (leftOp == "FLOT" and rightOp =="CTE_FLOAT") or (leftOp == "FLOAT" and rightOp == "FLOT"):
            print("float")
            return True
        else:
            print("Edge case", leftOp, rightOp)
            return False
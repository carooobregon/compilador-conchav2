class SemanticCube:
    def __init__(self):
        pass

    def validateType(self,leftOp, rightOp):
        if (leftOp == "INT" and rightOp =="CTE_ENT") or (leftOp == "INT" and rightOp == "INT") or (leftOp == "CTE_ENT" and rightOp =="CTE_ENT"):
            # print("CTE_ENT")
            return 'INT'
        elif (leftOp == "INT" and rightOp =="CTE_FLOAT") or (leftOp == "INT" and rightOp =="FLOT") :
            # print("float") 
            return 'FLOT'
        elif (leftOp == "STRING" and rightOp == "STRING") or (leftOp == "STRING" and rightOp == "STR") or (leftOp == "STR" and rightOp == "STRING"):
            # print("string")
            return 'STR'
        elif (leftOp == "STRING" and rightOp == "INT") or (leftOp == "STRING" and rightOp == "CTE_ENT") or (leftOp == "STRING" and rightOp == "FLOT") or (leftOp == "STRING" and rightOp == "CTE_FLOT"):
            # print("error")
            return 'STR' 
        elif (leftOp == "FLOT" and rightOp =="CTE_FLOAT") or (leftOp == "FLOT" and rightOp == "FLOT") or (leftOp == "FLOT" and rightOp == "INT") or (leftOp == "FLOT" and rightOp == "CTE_ENT") or (leftOp == "CTE_FLOAT" and rightOp =="CTE_FLOAT"):
            # print("float")
            return 'FLOT'
        elif (leftOp == "BOOL" and rightOp == "BOOL"):
            return 'BOOL'
        else:
            print("Edge case", leftOp, rightOp)
            return 'ERROR'
from Parser.UtilFuncs import UtilFuncs

class SemanticCube:
    Parser = UtilFuncs()
    def __init__(self):
        pass

    def validateType(self,leftOp, rightOp):
        if (leftOp == "INT" and rightOp =="CTE_ENT") or (leftOp == "INT" and rightOp == "INT") or (leftOp == "CTE_ENT" and rightOp =="CTE_ENT"):
            return 'INT'
        elif (leftOp == "INT" and rightOp =="CTE_FLOAT") or (leftOp == "INT" and rightOp =="FLOT") :
            return 'FLOT'
        elif (leftOp == "STRING" and rightOp == "STRING") or (leftOp == "STRING" and rightOp == "STR") or (leftOp == "STR" and rightOp == "STRING") or (leftOp == "STR" and rightOp == "STR"):
            return 'STR'
        elif (leftOp == "STRING" and rightOp == "INT") or (leftOp == "STRING" and rightOp == "CTE_ENT") or (leftOp == "STRING" and rightOp == "FLOT") or (leftOp == "STRING" and rightOp == "CTE_FLOT"):
            return 'STR' 
        elif (leftOp == "FLOT" and rightOp =="CTE_FLOAT") or (leftOp == "FLOT" and rightOp == "FLOT") or (leftOp == "FLOT" and rightOp == "INT") or (leftOp == "FLOT" and rightOp == "CTE_ENT") or (leftOp == "CTE_FLOAT" and rightOp =="CTE_FLOAT"):
            return 'FLOT'
        elif (leftOp == "BOOL" and rightOp == "BOOL"):
            return 'BOOL'
        else:
            print("Edge case", leftOp, rightOp)
            raise Exception("EXC Types", leftOp, "and", rightOp, "not compatible")
    
    def validateOperationBool(self, leftOp, rightOp):
        leftOp = self.Parser.convertTypes(leftOp)
        rightOp = self.Parser.convertTypes(rightOp)
        if (leftOp == "INT" and rightOp =="CTE_ENT") or (leftOp == "INT" and rightOp == "INT") or (leftOp == "CTE_ENT" and rightOp =="CTE_ENT"):
            return True
        elif (leftOp == "INT" and rightOp =="CTE_FLOAT") or (leftOp == "INT" and rightOp =="FLOT") :
            return True
        elif (leftOp == "STRING" and rightOp == "STRING") or (leftOp == "STRING" and rightOp == "STR") or (leftOp == "STR" and rightOp == "STRING") or (leftOp == "STR" and rightOp == "STR"):
            return False
        elif (leftOp == "STRING" and rightOp == "INT") or (leftOp == "STRING" and rightOp == "CTE_ENT") or (leftOp == "STRING" and rightOp == "FLOT") or (leftOp == "STRING" and rightOp == "CTE_FLOT"):
            return False 
        elif (leftOp == "FLOT" and rightOp =="CTE_FLOAT") or (leftOp == "FLOT" and rightOp == "FLOT") or (leftOp == "FLOT" and rightOp == "INT") or (leftOp == "FLOT" and rightOp == "CTE_ENT") or (leftOp == "CTE_FLOAT" and rightOp =="CTE_FLOAT"):
            return True
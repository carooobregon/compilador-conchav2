import csv

class VirtualMachine:
	losQuads = []
	losFuncs = []
	instructionPointer = 0
	paramsPointer = 0 

	def __init__(self):
		self.losFuncs = []
		self.losQuads = []
		pass

	def parseQuads(self):
		print(self.losQuads)
		startingPoint = self.losQuads[0][1]
		cont = startingPoint-1
		while (cont < len(self.losQuads)):
			currQuad = self.losQuads[cont]
			op = currQuad[0]
			if op < 6:
				self.handleOperations(currQuad)
			elif op < 10:
				self.handleTrueFalseOperations(currQuad)
			elif op < 12:
				cont = self.handleStackJumps(currQuad)
				continue
			elif op < 18:
				self.handleFunctionOps(currQuad)
			elif op < 19:
				self.handleOtherOperations(currQuad)
			cont+=1


	def runVM(self):
		self.handleFiles()
		self.createGlobalScope()
		self.parseQuads()

	def createGlobalScope(self):
		print(self.losQuads)

	def handleFiles(self):
		with open("quadruples.csv") as file:
			file = csv.reader(file)
			for row in file:
				cont = 0
				r = []
				while(cont < len(row)):
					curr = row[cont]
					curr = curr.replace("[",'')
					curr = curr.replace("]",'')
					curr = curr.replace("''",'')
					curr = curr.replace(" ",'')
					if curr.isdigit():
						curr = int(curr)
					cont += 1
					r.append(curr)
				self.losQuads.append(r)
		
		with open("funcTable.csv") as file:
			file = csv.reader(file)
			for row in file:
				self.losFuncs.append(row)
				cont = 0
				while(cont < len(row)):
					if row[cont].isdigit():
						row[cont] = int(row[cont])
					cont+=1
			
	def handleOperations(self, q):
		print("aqui ", q)
		if(q[0] == 1):#sum
			return q[1] + q[2]

		elif(q[0] == 2):#sub
			return q[1] - q[2]

		elif(q[0] == 3):#mul
			return q[1] * q[2]

		elif(q[0] == 4):#div
			return q[1] / q[2]

		elif(q[0] == 5): # q[1] = q[2] asignacion
			result =  q[2]

	def handleTrueFalseOperations(self,q):
		if(q[0] == 6): # morethan
			result = q[1] < q[2]

		elif(q[0] == 7): #lessthan
			result = q[1] > q[2]

		elif(q[0] == 8): #notequal
			result = q[1] != q[2]

		elif(q[0] == 9):#equal
			result = q[1] == q[2]

	def handleStackJumps(self,q):
		if(q[0] == 10):#goto
			return q[1] - 1

		elif(q[0] == 11):#gotof
			print("gotof")
			# if not access memory to look up self.losQuads[2] bool val 
			# 	i = self.losQuads[1]
			# else:
			# 	continue
			return q[1] - 1
	
	def handleFunctionOps(self,q):
		if(q[0] == 12):#end
			print("end")

		elif(q[0] == 13):#parameter
			print("parm")

		elif(q[0] == 14):#write
			print(self.losQuads[1])

		elif(q[0] == 15):#endfunc
			print("endfunc")

		elif(q[0] == 16):#era
			print("era")

		elif(q[0] == 17):#gosub
			print("gosub")

	def handleOtherOperations(self,q):
		if(q[0] == 18):#return
			print("ret")
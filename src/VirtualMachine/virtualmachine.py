from ast import parse
import csv
import math
from MemoriaVM import MemoriaVM
from Stack import Stack
from numpy.lib.shape_base import split

class VirtualMachine:
	RANGES = [0, 250, 500, 750]
	losQuads = []
	losFuncs = {}
	instructionPointer = 0
	paramsPointer = 0 
	memoriaStack = Stack()
	currMemoria = ""
	globalMemoria = MemoriaVM([0 for i in range(12)], "temp")
	currMemoria = MemoriaVM([0 for i in range(12)], "temp")
	currScope = ""
	migajitas = Stack()
	newMemory = ""
	

	def __init__(self):
		self.losFuncs = {}
		self.losQuads = []
		self.losConsts = []
		pass

	# def parseQuads(self):
	# lookupConst
	def runVM(self):
		self.handleFiles()
		self.createGlobalScope()
		self.runQuads()
		
	def createGlobalScope(self):
		self.globalMemoria = MemoriaVM(self.losFuncs['global'], 'global')
		self.currMemoria = self.globalMemoria
		self.memoriaStack.push(self.globalMemoria)

	def handleFiles(self):
		self.parseQuadruples()
		self.parseFunctions()
		self.parseConstTable()

	def parseQuadruples(self):
		with open("quadruples.csv") as file:
			file = csv.reader(file)
			for row in file:
				temp = []
				cont = 0
				while(cont < len(row)):
					row[cont] = row[cont].replace("[","")
					row[cont] = row[cont].replace("]","")
					row[cont] = row[cont].replace(" ","")
					if row[cont].isdigit():
						row[cont] = int(row[cont])
					elif isinstance(row[cont],str):
						row[cont] = row[cont].replace("\'", "")
					cont+=1
				self.losQuads.append(row)

	## nice to have q no sea un dict
	def parseFunctions(self):
		with open("funcTable.csv") as file:
			file = csv.reader(file)
			for row in file:
				cont = 1
				while(cont < len(row)):
					if row[cont].isdigit():
						row[cont] = int(row[cont])
					elif isinstance(row[cont],str):
						row[cont] = row[cont].replace("\'", "")
					cont+=1
				self.losFuncs[row[0]] = row[1:]
	
	def checknumber(self,a):
		try:
			a=float(a)
			if a == 0:
				return a
			if int(a)/a==1:
				return int(a)
			elif a/int(a)>1:
				return float(a)
		except ValueError:
			return str(a)

	def parseConstTable(self):
		with open("constTable.csv") as file:
			file = csv.reader(file)
			for row in file:
				elem = self.checknumber(row[0])
				self.losConsts.append(elem)

	def runQuads(self):
			# print(self.losQuads)
			startingPoint = self.losQuads[0][1]
			cont = startingPoint-1
			while (cont < len(self.losQuads)):
				currQuad = self.losQuads[cont]
				op = currQuad[0]
				if op < 6:
					self.handleOperations(currQuad)
				elif op < 10:
					self.handleTrueFalseOperations(currQuad)
				elif op < 15:
					cont = self.handleStackJumps(currQuad, cont)
					continue
				elif op < 18:
					self.handleFunctionOps(currQuad)
				else:
					cont = self.handleOtherOperations(currQuad, cont)
					continue
				cont+=1

	def lookupConst(self, address):
		add = address % 4000
		valor = 0
		if add < self.RANGES[1]:
			return self.losConsts[add]
			
		if add < self.RANGES[2]:
			return self.losConsts[add]
			
		if add < self.RANGES[3]:
			return self.losConsts[add] 
		else:
			return self.losConsts[add]

	def lookUpVal(self, dir):
		if dir >= 4000:
			val = self.lookupConst(dir)
		elif dir >= 2000:
			val = self.currMemoria.lookupElement(dir)
		elif dir >= 1000:
			val = self.globalMemoria.lookupElement(dir)
		return val
	
	def assignVal(self, dir, val):
		if dir < 2000:
			self.globalMemoria.asignElement(dir, val)
		else:
			self.currMemoria.asignElement(dir, val)
			
	def handleOperations(self, q):
		val = self.lookUpVal(q[1])
		if(q[0] == 5): # q[1] = q[2] asignacion
			self.assignVal(q[2], val)
			return

		val2 = self.lookUpVal(q[2])
		if(q[0] == 1):#sum
			self.assignVal(q[3], val+val2)

		elif(q[0] == 2):#sub
			self.assignVal(q[3], val-val2)

		elif(q[0] == 3):#mul
			self.assignVal(q[3], val*val2)

		elif(q[0] == 4):#div
			self.assignVal(q[3], val/val2)

	def handleTrueFalseOperations(self,q):
		val = self.lookUpVal(q[1])
		val2 = self.lookUpVal(q[2])
		
		if(q[0] == 6): # morethan
			self.assignVal(q[3], val < val2)

		elif(q[0] == 7): #lessthan
			self.assignVal(q[3], val > val2)

		elif(q[0] == 8): #notequal
			self.assignVal(q[3], val != val2)

		elif(q[0] == 9):#equal
			self.assignVal(q[3], val == val2)

	def handleStackJumps(self,q, cont):
		if(q[0] == 10):#goto
			return q[1] - 1

		elif(q[0] == 11):#gotof
			val = self.lookUpVal(q[2])
			return q[1] - 1 if not self.lookUpVal(q[2]) else cont + 1
		
		elif(q[0] == 12):#end
			print("end") # liberar mem todo
			return 1000
			
		elif(q[0] == 13):#gosub
			self.currMemoria = self.newMemory
			self.memoriaStack.push(self.currMemoria)
			self.migajitas.push(cont + 1)
			dirFuncion = self.losFuncs[q[1]][1]
			return dirFuncion - 1

		elif(q[0] == 14):#endfunc
			self.memoriaStack.pop()
			self.currMemoria = self.memoriaStack.peek()
			return self.migajitas.pop()

	def handleFunctionOps(self,q):
		if(q[0] == 15):#era
			name = q[1]
			self.newMemory = MemoriaVM(self.losFuncs[name], name)

		elif(q[0] == 16):#write
			if q[1] >= 4000:
				val = self.lookupConst(q[1])
			elif q[1] >= 2000:
				val = self.currMemoria.lookupElement(q[1])
			elif q[1] >= 1000:
				val = self.globalMemoria.lookupElement(q[1])

			print(val)
			
		elif(q[0] == 17):#parameter
			## assign to memory
			# print("parm")
			val = ""
			if q[1] >= 4000:
				val = self.lookupConst(q[1])
			elif q[1] >= 2000:
				val = self.currMemoria.lookupElement(q[1])
			elif q[1] >= 1000:
				val = self.globalMemoria.lookupElement(q[1])
			
			self.newMemory.asignElement(q[2], val)
	
	def handleOtherOperations(self,q, cont):
		if(q[0] == 18):#return
			val = self.lookUpVal(q[1])
			self.assignVal(q[2], val)
			return cont + 1
		elif q[0] == 19:
			val = input()
			self.validateTypeAndAssign(q[1],val)
			return cont
		elif q[0] == 20:
			return q[1] -1

	def validateTypeAndAssign(self,address,val):
		inType = address % 1000
		if 0 <= inType <  250: # int
			try:
				check = int(val)
				self.assignVal(address, check)
			except ValueError:
				raise Exception("Wrong input type, trying to assign to int")

		elif 250 <= inType < 500: # float
			try:
				check = float(val)
				self.assignVal(address, check)
			except ValueError:
				raise Exception("Wrong input type, trying to assign to float")
		
		elif 500 <= inType < 750: # bool
			try:
				check = bool(val)
				self.assignVal(address, check)
			except ValueError:
				raise Exception("Wrong input type, trying to assign to boolean")
		
		else: # str
			self.assignVal(address, val)

	def printMemoria(self):
		print("Curr Memoria")
		self.currMemoria.printElements(self.currMemoria)
		# for i in self.currMemoria:
		# 	print(i)
		print("Global Mem")
		self.globalMemoria.printElements(self.globalMemoria)
		# for i in self.globalMemoria:
		# 	print(i)
		
		print("memoriaStack")
		# while not self.memoriaStack.isEmpty():
		# 	MemoriaVM.printElements(self,self.memoriaStack.pop())
			#MemoriaVM.printElements(self,i)
	
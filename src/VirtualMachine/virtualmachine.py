from ast import parse
import csv
import math
from MemoriaVM import MemoriaVM

from numpy.lib.shape_base import split

class VirtualMachine:
	losQuads = []
	losFuncs = {}
	instructionPointer = 0
	paramsPointer = 0 
	memoriaStack = []
	currMemoria = ""
	globalMemoria = ""

	def __init__(self):
		self.losFuncs = {}
		self.losQuads = []
		self.losConsts = []
		pass

	# def parseQuads(self):

	def runVM(self):
		self.handleFiles()
		self.createGlobalScope()
		self.globalMemoria.asignElement(1250, 80.30)
		print(self.globalMemoria.pruebaWhile(1250))

	def createGlobalScope(self):
		self.globalMemoria = MemoriaVM(self.losFuncs['global'], 'global')

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
					cont+=1
				self.losFuncs[row[0]] = row[1:]
	
	def parseConstTable(self):
		with open("constTable.csv") as file:
			file = csv.reader(file)
			for row in file:
				self.losConsts.append(row[0])
		
		# quitando puntos extra para ints que no son floats
		tempConst = []
		tempInts = []
		tempFlot = []
		tempStr = []
		tempBool = []		
		for i in self.losConsts:
			owo = i.split(' ')
			if(int(owo[1]) < 4250):
				# temp = owo[0] 
				# print("owo", int(owo[0]))
				# temp = temp[:-2]
				# print("temp",temp)
				tempInts.append(int(owo[0]))

			elif(int(owo[1]) < 4500): # float
				tempFlot.append(float(owo[0]))

			elif(int(owo[1]) < 4750): # bool
				tempBool.append(bool(owo[0]))
				print("pq bools constantes?")

			else: #str
				tempStr.append(owo[0])
				
		
		tempConst.append(tempInts)
		tempConst.append(tempFlot)
		tempConst.append(tempStr)
		
		self.losConsts = tempConst

		print("CONSTANTES")
		print(self.losConsts)


	def handleOperations(self):
		for q in self.losQuads:
			print(q)
			# operands
			if(q[0] == 1):#sum
				return q[1] + q[2]

			elif(q[0] == 2):#sub
				return q[1] - q[2]

			elif(q[0] == 3):#mul
				return q[1] * q[2]

			elif(q[0] == 4):#div
				return q[1] / q[2]

	def handleTrueFalseOperations(self):
		result = False
		for q in self.losQuads:
			print(q)
			if(q[0] == 5): # q[1] = q[2] asignacion
				result =  q[2]

			if(q[0] == 6): # morethan
				result = q[1] < q[2]

			elif(q[0] == 7): #lessthan
				result = q[1] > q[2]

			elif(q[0] == 8): #notequal
				result = q[1] != q[2]

			elif(q[0] == 9):#equal
				result = q[1] == q[2]
		return result

	def handleOtherOperations(self):
		for q in self.losQuads:
			print(q)
			if(q[0] == 5): # q[1] = q[2] asignacion
				result =  q[2]
			elif(q[0] == 18):#return
				print("ret")

	def handleStackJumps(self):
		i = 0
		while i < len(self.losQuads):
			print(self.losQuads[i])
			if(self.losQuads[0] == 10):#goto
				print("goto")
				i = self.losQuads[1]

			elif(self.losQuads[0] == 11):#gotof
				print("gotof")
				if not self.losQuads[2]:
					i = self.losQuads[1]
				else:
					continue

			elif(self.losQuads[0] == 12):#end
				print("end")

			elif(self.losQuads[0] == 13):#parameter
				print("parm")

			elif(self.losQuads[0] == 14):#write
				print(self.losQuads[1])

			elif(self.losQuads[0] == 15):#endfunc
				print("endfunc")

			elif(self.losQuads[0] == 16):#era
				print("era")

			elif(self.losQuads[0] == 17):#gosub
				print("gosub")

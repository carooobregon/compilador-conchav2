


import csv

def main():
	losQuads = []

	with open("myfile.csv") as file:
		file = csv.reader(file)
		for row in file:
			losQuads.append(row)
    

	for q in losQuads:
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

		elif(q[0] == 5): # q[1] = q[2] asignacion
			return  q[2]

		elif(q[0] == 6):# morethan
			temp = q[1] < q[2]
			return temp

		elif(q[0] == 7):#lessthan
			temp = q[1] > q[2]
			return temp

		elif(q[0] == 8):#notequal
			temp = q[1] != q[2]
			return temp

		elif(q[0] == 9):#equal
			temp = q[1] == q[2]
			return temp

		elif(q[0] == 10):#goto
			print("goto")
			return q[1]

		elif(q[0] == 11):#gotof
			print("gotof")
			if not q[2]:
				return q[1]
			else:
				continue
			
		elif(q[0] == 12):#end
			print("end")

		elif(q[0] == 13):#parameter
			print("parm")

		elif(q[0] == 14):#write
			return print(q[1])

		elif(q[0] == 15):#endfunc
			print("endfunc")

		elif(q[0] == 16):#era
			print("era")

		elif(q[0] == 17):#gosub
			print("gosub")

		elif(q[0] == 18):#return
			print("ret")
		
		

	
	
	







if __name__=='__main__':
    main()
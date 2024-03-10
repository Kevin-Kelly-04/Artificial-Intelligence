import sys

#taking input from stdin and splitting them up into their defind 
def input():
	ui = sys.stdin.read().split('\n')
	A = initializeMatrix(ui[0].split())
	B = initializeMatrix(ui[1].split())
	pi = initializeMatrix(ui[2].split())
	return A, B, pi

#taking the list notations and transforming them into their respective matrices
def initializeMatrix(matrix):
	row = int(matrix.pop(0))
	col = int(matrix.pop(0))
	mat = []
	idx = 0
	for i in range(row):
		a = []
		for j in range(col):
			a.append(float(matrix[idx]))
			idx += 1
		mat.append(a)
	return mat

#multiplying two matrices
def multiply(A, B):
	result = []
	result = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]
	return result
	
# emission probability after state transition
def emissionProb():
	A, B, pi = input()
	#s = mult(pi, A)
	pi_A = multiply(pi, A)
	print(pi_A)
	pi_A_B = multiply(pi_A, B)
	pi_A_B_round = [str(round(col, 2)) for row in pi_A_B for col in row]
	size = str(len(pi_A_B)) + " " + str(len(pi_A_B[0]))
	output = size + " " + ' '.join(pi_A_B_round)
	print(output)
	

def mult(A, B):
	ret = []
	print("-----------")
	print("A = ", A)
	print("B = ", B)
	print("-----------")
	for A_row in A:
		res = []
		print("Arow = ", A_row)
		print("++++++++++")
		print("B zip = ", zip(*B))
		for B_col in zip(*B):
			print("B col = ", B_col)
			print("++++++++")
			summ = 0
			for a, b in zip(A_row, B_col):
				summ += a*b
			res.append(summ)
		ret.append(res)
	print(ret)
	return ret

emissionProb()


import sys

#taking input from stdin and splitting them
def input():
	ui = sys.stdin.read().split('\n')
	A = initializeMatrix(ui[0].split())
	B = initializeMatrix(ui[1].split())
	pi = initializeMatrix(ui[2].split())
	emission = emissions(ui[3].split())
	return A, B, pi, emission

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

#get emissions sequence
def emissions(matrix):
	return [int(i) for i in matrix[1:]]

#multiplying two matrices
def multiply(A, B):
	result = []
	result = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]
	return result

#multiplying two vectors
def multiply_vect(A, B):
	vect = []
	for a, b in zip(A, B):
		vect.append(a*b)
	return vect

#getting observation sequence
def current_emission(B, emis):
	return [row[emis] for row in B]

def forward(A, B, emission, alpha, idx):
	#if emission sequence is over (basecase) then sum alpha vector and return
	if idx == len(emission):
		final_alpha = round(sum(alpha), 6)
		return final_alpha
	curr_emis = current_emission(B, emission[idx])
	#multiply most recent calculated alpha vector with A matrix
	curr_alpha = multiply([alpha], A)
	print(curr_alpha)
	#multiply (alpha*A) with current observation vector
	new_alpha = multiply_vect(curr_alpha[0],  curr_emis)
	return forward(A, B, emission, new_alpha, idx+1)

#initialize pi, transition matrix, observation matrix and and emission sequence
A, B, pi, emission = input()
#initialize alpha
init_alpha = multiply_vect(pi[0], current_emission(B, emission[0]))
final_alpha = forward(A, B, emission, init_alpha, idx=1)
print(final_alpha)
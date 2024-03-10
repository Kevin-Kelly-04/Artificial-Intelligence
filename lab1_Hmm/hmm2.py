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

def emissions(matrix):
	return [int(i) for i in matrix[1:]]

#getting the dot product of two matrices
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


def current_emission(B, emis):
	return [row[emis] for row in B]


def viterbi2(A, B, emission, beta, max_ind, idx):
	if idx == len(emission):
		max_ind.append(beta.index(max(beta)))
		print("")
		print(*max_ind, sep = " ")
		return

	current_emis = current_emission(B, emission[idx])
	max_prob = []
	ind = []
	for i in range(len(A)):
		temp = []
		A_col = current_emission(A, i)
		for j in range(len(A_col)):
			temp.append(beta[j] * A_col[j] * current_emis[i] ) 
		max_prob.append(max(temp))
		ind.append(temp.index(max(temp)))
	temp_ind = max_prob.index(max(max_prob))
	max_ind.append(ind[temp_ind])
	return viterbi2(A, B, emission, max_prob, max_ind, idx+1)


def viterbi(A, B, emission, delta, max_ind, idx):
	#backtracking
    #backtracking
    if idx == len(emission):
        #print(max_ind)
        #print(delta)
        states = []
        state_idx = delta.index(max(delta))
        #print(state_idx)
        states.append(state_idx)

        #proceed backwards through the saved max index lists 
        i = len(max_ind) - 1
        while i > 0:
            states.insert(0, max_ind[i][state_idx])
            state_idx = max_ind[i][state_idx]
            i -= 1
        print(*states, sep = " ")

        return

    current_emis = current_emission(B, emission[idx])
    max_prob = []
    ind = []
    for i in range(len(A)):
        temp = []
        A_col = current_emission(A, i)
        for j in range(len(A_col)):
            temp.append(delta[j] * A_col[j] * current_emis[i])
        max_prob.append(max(temp))
        ind.append(temp.index(max(temp)))
    max_ind.append(ind)
    return viterbi(A, B, emission, max_prob, max_ind, idx+1)


#initialize pi and emission sequence
A, B, pi, emission = input()

#initialize beta
init_delta = multiply_vect(pi[0], current_emission(B, emission[0]))

max_ind = [[0] * len(A)]
#viterbi2(A, B, emission, init_delta, max_ind, idx=1)
viterbi(A, B, emission, init_delta, max_ind, idx=1)


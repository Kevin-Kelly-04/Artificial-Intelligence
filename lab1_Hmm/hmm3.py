import sys
import math

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
	#multiply (alpha*A) with current observation vector
	new_alpha = multiply_vect(curr_alpha[0],  curr_emis)
	return forward(A, B, emission, new_alpha, idx+1)

# implementation of baum welch algorithm as via stamp tutorial
def baum_welch(A, B, pi, emission):
	T = len(emission)
	N = len(A)
	M = len(B[0])

	c = [0] * T
	alpha = [[None for i in range(N)] for j in range(T)]
	beta = [[None for i in range(N)] for j in range(T)]
	gamma = [[None for i in range(N)] for j in range(T)]
	di_gamma = [[[None for i in range(N)] for j in range(N)] for k in range(T)]
	logprob = -999999
	oldlogprob = -9999999

	iters = 0
	maxIters = 10000

	while(iters < maxIters and ( abs(logprob - oldlogprob) > 0.00001) ):

		#---------------Alpha pass--------------

		# compute α0(i)
		c[0] = 0
		B_i_0 = current_emission(B, emission[0])
		for i in range(0, N):
			alpha[0][i] = pi[i]*B_i_0[i]
			c[0] = c[0] + alpha[0][i]

		# scale the α0(i)
		c[0] = 1/c[0]
		for i in range(0, N):
			alpha[0][i] = c[0] * alpha[0][i]

		# compute αt(i)
		for t in range(1, T):
			B_i_1_T = current_emission(B, emission[t])
			c[t] = 0
			for i in range(0, N):
				alpha[t][i] = 0
				for j in range(0, N):
					alpha[t][i] += alpha[t-1][j]*A[j][i]
				alpha[t][i] = alpha[t][i] * B_i_1_T[i]
				c[t] = c[t] + alpha[t][i]

			# scale αt(i)
			c[t] = 1/c[t]
			for s in range(0, N):
				alpha[t][s] = alpha[t][s] * c[t]

		# ---------------Beta pass------------------

		#  Let βT −1(i) = 1, scaled by cT −1
		for i in range(0, N):
			beta[T-1][i] = c[T-1]

		# β-pass
		for t in range(T-2, -1, -1):
			B_i_t1 = current_emission(B, emission[t+1])
			for i in range(0, N):
				beta[t][i] = 0
				for j in range(0, N):
					beta[t][i] = beta[t][i] + (A[i][j] * B_i_t1[j] * beta[t+1][j])

				#scale βt(i) with same scale factor as αt(i)
				beta[t][i] = c[t]*beta[t][i]


		# -------------Compute γt(i, j) and γt(i)-------------

		for t in range(0, T-1):
			B_i_t1 = current_emission(B, emission[t+1])
			for i in range(0, N):
				gamma[t][i] = 0
				for j in range(0, N):
					di_gamma[t][i][j] = alpha[t][i]*A[i][j]*B_i_t1[j]*beta[t+1][j]
					gamma[t][i] = gamma[t][i] + di_gamma[t][i][j]

		# Special case for γT −1(i) (as above, no need to normalize)
		for i in range(0, N):
			gamma[T-1][i] = alpha[T-1][i]

		# ---------------Re-estimate A, B and π-------------

		# re-estimate π
		for i in range(0, N):
			pi[i] = gamma[0][i]
			#print(" pi = " + str(pi[i]))

		# re-estimate A
		for i in range(0, N):
			denom = 0
			for t in range(0, T-1):
				denom = denom + gamma[t][i]
			for j in range(0, N):
				numer = 0
				for t in range(0, T-1):
					numer = numer + di_gamma[t][i][j]
				A[i][j] = numer/denom
				#print(A[i][j])

		#  re-estimate B
		for i in range(0, N):
			denom = 0
			for t in range(0, T):
				denom = denom + gamma[t][i]
			for j in range(0, M):
				numer = 0
				for t in range(0, T):
					if emission[t] == j:
						numer = numer + gamma[t][i]
				B[i][j] = numer/denom

		# Compute log[P(O | λ)]
		oldlogprob = logprob
		logprob = 0
		for i in range(0, T):
			logprob = logprob + math.log(c[i])
		logprob = -logprob

		# To iterate or not to iterate, that is the question
		iters = iters + 1
		print(iters)
	print("iterations = ", iters)	
	estimatedA = A
	estimatedB = B
	estimatedPi = pi
	return(estimatedA, estimatedB, estimatedPi)


#initialize pi, transition matrix, observation matrix and and emission sequence
A, B, pi, emission = input()
estA, estB, estPi = baum_welch(A, B, pi[0], emission)
finalA = [] 
finalB = []
finalPi = []
finalA.append(len(estA))
finalA.append(len(estA[0]))
finalB.append(len(estB))
finalB.append(len(estB[0]))
finalPi.append(len(estPi))

for i in range(0, len(estA)):
	for j in range(0, len(estA[0])):
		finalA.append(round(estA[i][j], 3))

for i in range(0, len(estB)):
	for j in range(0, len(estB[0])):
		finalB.append(round(estB[i][j], 3))

for i in range(0, len(estPi)):
	finalPi.append(round(estPi[i], 3))

print(*finalA, sep = " ")
print(*finalB, sep = " ")
print(*finalPi, sep = " ")


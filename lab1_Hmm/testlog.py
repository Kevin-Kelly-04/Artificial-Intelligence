import math
import numpy as np

a = [[0.698, 0.012, 0.289] [0.101, 0.812, 0.087] [0.191, 0.302, 0.507]]
b = np.matrix('0.7 0.05 0.25; 0.1 0.8 0.1; 0.2 0.3 0.5')
a = np.log(a)
b = np.log(b)

for row in range(len(a)):
	for col in range(len(a[row])):
		print(a[row][col])

dist = np.linalg.norm(a-b)
print(dist)

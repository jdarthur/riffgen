import random

def choose_weighted(choices, weights) :
	"""
	choose a thing from a list based on weights

	TODO: make this a less trash implementation

	"""

	total = 0
	for i in weights :
		total = total + i
	selection = random.randint(0, total -1)
	bucket = []
	for i in range(0, len(choices)) :
		for j in range(0, weights[i]) :
			bucket.append(choices[i])
	return(bucket[selection])


"""
options = ['a', 'b', 'c', 'd']
weights = [10, 20, 100, 10] 

op_d = {} 
for o in options :
	op_d[o] = 0

for i in range(0, 1000) :
	choice = choose_weighted(options, weights)
	op_d[choice] += 1

print(op_d)
"""
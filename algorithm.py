import sys as sys
from branching import Algorithm1

import helper
import copy
from bruteforce import BruteForce

def maximise(cb = None, input = None, output = None, minimum = None):
	#po, k, V_2, c
	#variables 
	#output : output data structure for cb() to populate. This is an empty List Partial Ordering to be populated 
	#max_k : maximal bound for binary search (that is, the maximal number 
	#            of crossings for bipartite graph G)
	#cb    : callback function to run binary search on (that is, the branching algo we execute)
	#output: 

	#execute binary search to find maximal k.
	left = 0
	input2 = copy.deepcopy(input)
	if cb:
		if cb(0, input2, output) == True:
			return 0
		output.clear()
		input2 = copy.deepcopy(input)
		m = 1 #first find maximal m 
		while m < minimum or not cb(m, input2, output):
			output.clear()
			input2 = copy.deepcopy(input)
			left = m
			m = 2*m
		right = m
		
		while left < right:
			output.clear()
			mid = left + (right - left + 1) // 2  # Adding 1 to ensure rounding up
			input2 = copy.deepcopy(input)
			if cb(mid, input2, output) == False:
				left = mid
			else:
				right = mid - 1
		return left + 1

#main 
def main():
	if len(sys.argv) == 0: 
		print("No inputs")
		return
	
	#input = (G, V_1, V_2)
	input = helper.readInput(sys.argv[1])
	V_2 = input[2]
	V_1 = input[1]
	G = input[0]
	Isolated = input[3]
	c = {}
	minimum = helper.computeAllCrossings(c, G, V_2, V_1)
	incomparable = {}
	for a in V_2:
		incomparable[a] = []
		for b in V_2:
			if a == b:
				continue 
			incomparable[a].append(b)

	input2 = (G, V_1, V_2, c, incomparable)
	po = {}

	k = maximise(Algorithm1, input2, po, minimum)
	r = Algorithm1(k, input2, po)
	out = helper.writeOutput(V_2, po)

	out = out + Isolated
	#print(out)
	for v in out:
		print(v)

#execute
if __name__ == "__main__":
	main()
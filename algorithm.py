import sys as sys
from branching import branching_algorithm, incomparable, RRL01, RRL02, RRlarge

import helper
import copy
from bruteforce import BruteForce

#Simplification Rules

def RR1(po, V_2, c, k):
	#any pair of vertices {a.b} in V_2 that form a 0/j pattern,
	#commit a < b to the Poset. 
	n = len(V_2)
	for a in range(n):
		for b in range (a, n):
			if(a != b):
				if not incomparable(po, V_2[a], V_2[b]):
					continue
				c_ab = helper.getCrossings(V_2[a],V_2[b], c)
				c_ba = helper.getCrossings(V_2[b],V_2[a], c)			
				if((c_ab == 0) and (c_ba > 0)): # commit a < b
					k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k , c, V_2)
					#po[V_2[a]].append(V_2[b])
				elif((c_ba == 0) and (c_ab > 0)): # commit b < a
					k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c, V_2)
					#po[V_2[b]].append(V_2[a])
				if c_ab == 0 and c_ba == 0:
					k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c, V_2)
				if k < 0:
					return k

	 		
	return k

def RR2(k, po, V_2, G, c):
	#any pair of vertices {a,b} in V_2 such that N(a)\{a} = N(b)\{b}
	#commit a < b to Poset and do parameter accounting k = k - c_ab

	n = len(V_2)
	for a in range(n):
		for b in range (a, n):
			if(a != b):
				if not incomparable(po, V_2[a], V_2[b]):
					continue
				cnb_a = helper.graph_getClosedNeighbourhood(V_2[a], G)
				cnb_b = helper.graph_getClosedNeighbourhood(V_2[b], G)
				cnb_a.remove(V_2[a])
				cnb_b.remove(V_2[b])
				if cnb_a == cnb_b :
					#po[V_2[a]].append(V_2[b])
					k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c, V_2)
				if k < 0:
					return k
	return k

def RR3(k, po, V_2, c):
	#for each pair of vertices {b,a} that form a 2/1 pattern
	#commit a<b to the Poset and do param accounting 
	n = len(V_2)
	for a in range (n):
		for b in range(a+1, n):
			if not incomparable(po, V_2[a], V_2[b]):
				continue
			c_ab = helper.getCrossings(V_2[a], V_2[b], c)
			c_ba = helper.getCrossings(V_2[b], V_2[a], c)
			if (c_ab == 1) and (c_ba == 2):
				k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c, V_2)	
			if k < 0:
				return k
	return k


#takes in empty partial ordering, callback function that is the branching algorithm. 
#executes branching algorithm in a binary search  manner to find k that is minimal. 
def minimise1(k_max, cb = None, input = None, output = None):
#po, k, V_2, c
	#variables 
	#output : output data structure for cb() to populate. This is an empty List Partial Ordering to be populated 
	#max_k : maximal bound for binary search (that is, the maximal number 
	#            of crossings for bipartite graph G)
	#cb    : callback function to run binary search on (that is, the branching algo we execute)
	#output: 

	#execute binary search to find minimal k. 
	left = 0
	right = k_max
	input2 = copy.deepcopy(input)
	if cb:
		while left < right:
			mid = left + (right - left + 1) // 2  # Adding 1 to ensure rounding up
			#output = {}
			input2 = copy.deepcopy(input)
			if cb(mid, input2, output) == False:
				left = mid
			else:
				right = mid - 1
			if output:
				output.clear()
		
		#i = 0
		#input2 = copy.deepcopy(input)
		#while not cb(i, input2, output):
		#	i += 1
		#	output.clear()
		#	input2 = copy.deepcopy(input)

		##left is maximal value that returns false
		#input = copy.deepcopy(input2)
		return left + 1
		#return i

def minimise(cb = None, input = None, output = None):
#po, k, V_2, c
	#variables 
	#output : output data structure for cb() to populate. This is an empty List Partial Ordering to be populated 
	#max_k : maximal bound for binary search (that is, the maximal number 
	#            of crossings for bipartite graph G)
	#cb    : callback function to run binary search on (that is, the branching algo we execute)
	#output: 

	#execute binary search to find minimal k.

	left = 0
	#right = k_max
	input2 = copy.deepcopy(input)
	if cb:
		if cb(0, input2, output) == True:
			return 0
		m = 1 #first find maximal m 
		while not cb(m, input2, output):
			output.clear()
			input2 = copy.deepcopy(input)
			left = m
			m = 2*m
		right = m
		
		while left < right:
			mid = left + (right - left + 1) // 2  # Adding 1 to ensure rounding up
			input2 = copy.deepcopy(input)
			if cb(mid, input2, output) == False:
				left = mid
			else:
				right = mid - 1

			output.clear()
		
		

		#i = 0
		#input2 = copy.deepcopy(input)
		#while not cb(i, input2, output):
		#	i += 1
		#	output.clear()
		#	input2 = copy.deepcopy(input)

		##left is maximal value that returns false
		#input = copy.deepcopy(input2)
		return left + 1
		#return i

def Kernalize(G, V_2, po, k, c):
	#apply exhaustively
	prevK = -1
	while prevK != k: 
		prevK = k
		#print("got here")
		k = RR1(po, V_2, c, k)
		#print("got here")
		k = RR2(k, po, V_2, G, c)

	#apply RRL01 RRL02 and RRlarge exhaustivaly 
	prevK = -1
	while prevK != k:
		prevK = k
		RRL01(po, V_2)
		k = RRL02(po, V_2, c, k)
		k = RRlarge(po, V_2, c, k)
	return k
	
 
def Algorithm1 (k, input, output):
	#unpack inputs
	G = input[0]
	V_1 = input[1]
	V_2 = input[2]
	c = input[3]
	for key in G.keys():
		output[key] = []
	



	k = Kernalize(G, V_2, output, k, c)
	if k < 0:
		return False
	#apply RR3 exhaustively
	prevK = -1
	while prevK != k:
		prevK = k
		k = RR3(k, output, V_2, c)
		if k < 0:
			return False

	r = branching_algorithm(output, k, V_2, c)
	return r

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
	helper.computeAllCrossings(c, G, V_2, V_1)
	input2 = (G, V_1, V_2, c)
	
	#k_max = 20 #<=== need to fix this once validated branching 
	n = len(V_2)
	m = len(V_1)
	k_max = int(((n*(n-1))/2)*((m*(m-1))/2))
	po = {}

	k = minimise(Algorithm1, input2, po)
	r = Algorithm1(k, input2, po)
	out = helper.writeOutput(V_2, po)
	out = out + Isolated
	for v in out:
		print(v)

#execute
#main()

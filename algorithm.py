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
					k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k , c)
					#po[V_2[a]].append(V_2[b])
				elif((c_ba == 0) and (c_ab > 0)): # commit b < a
					k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c)
					#po[V_2[b]].append(V_2[a])
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
					k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c)
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
				helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c)	
	return k


#takes in empty partial ordering, callback function that is the branching algorithm. 
#executes branching algorithm in a binary search  manner to find k that is minimal. 
def minimise(k_max, cb = None, input = None, output = None):
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

		#left is maximal value that returns false
		input = copy.deepcopy(input2)
		return left + 1

def Kernalize(G, V_2, po, k, c):
	#apply exhaustively
	prevK = -1
	while prevK != k: 
		prevK = k
		k = RR1(po, V_2, c, k)
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
	c = {}
	for key in G.keys():
		output[key] = []
	helper.computeAllCrossings(c, G, V_2, V_1)

	k = Kernalize(G, V_2, output, k, c)
	#apply RR3 exhaustively
	prevK = -1
	while prevK != k:
		prevK = k
		k = RR3(k, output, V_2, c)

	r = branching_algorithm(output, k, V_2, c)
	return r

def isTransitiveWrtX(po, a, b, x):
	#if {a,x} xor {b,x} is comparable (but not both)
	comparableAX = False
	comparableBX = False
	comparableAX = not incomparable(po, a, x)
	comparableBX = not incomparable(po, b, x)

	comparable = False 
	comparable = (comparableAX and not comparableBX) or (not comparableAX and comparableBX)

	return comparable 

def isTransitive(po, a, b, V_2):
	for vertex in V_2:
		if a == vertex or b == vertex:
			continue
		if isTransitiveWrtX(po, a, b, vertex):
			return True
	return False

#main 
def main():
	if len(sys.argv) == 0: 
		print("No inputs")
		return
	
	#input = (G, V_1, V_2)
	input = helper.readInput(sys.argv[1])
	V_2 = input[2]
	V_1 = input[1]
	
	#k_max = 20 #<=== need to fix this once validated branching 
	n = len(V_2)
	m = len(V_1)
	k_max = int(((n*(n-1))/2)*((m*(m-1))/2))
	po = {}

	k = minimise(k_max, Algorithm1, input, po)
	Algorithm1(k, input, po)
	out = helper.writeOutput(V_2, po)
	for v in out:
		print(v)


#execute
main()

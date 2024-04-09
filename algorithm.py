import sys as sys
from branching import branching_algorithm
import helper

#Simplification Rules
def RR1(po, V_2, c):
	#any pair of vertices {a.b} in V_2 that form a 0/j pattern,
	#commit a < b to the Poset. 
	n = len(V_2)
	for a in range(n):
		for b in range (a, n):
			if(a != b):
				c_ab = helper.getCrossings(V_2[a],V_2[b], c)
				c_ba = helper.getCrossings(V_2[b],V_2[a], c)			
				if((c_ab == 0) and (c_ba > 0)): # commit a < b
					helper.insertPartialOrdering(po, V_2[a], V_2[b])
					#po[V_2[a]].append(V_2[b])
				elif((c_ba == 0) and (c_ab > 0)): # commit b < a
					helper.insertPartialOrdering(po, V_2[b], V_2[a])
					#po[V_2[b]].append(V_2[a])

def RR2(k, po, V_2, G, c):
	#any pair of vertices {a,b} in V_2 such that N(a)\{a} = N(b)\{b}
	#commit a < b to Poset and do parameter accounting k = k - c_ab

	n = len(V_2)
	for a in range(n):
		for b in range (a, n):
			if(a != b):
				cnb_a = helper.graph_getClosedNeighbourhood(V_2[a], G)
				cnb_b = helper.graph_getClosedNeighbourhood(V_2[b], G)
				cnb_a.remove(V_2[a])
				cnb_b.remove(V_2[b])
				if cnb_a == cnb_b :
					#po[V_2[a]].append(V_2[b])
					helper.insertPartialOrdering(po, V_2[a], V_2[b])
					k = k - helper.getCrossings(V_2[a], V_2[b], c)
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
	if cb:
		while left < right:
			mid = left + (right - left + 1) // 2  # Adding 1 to ensure rounding up
			if cb(mid, input, output) == False:
				left = mid
			else:
				right = mid - 1

		#left is maximal value that returns false
		return left + 1

def Kernalize(G, V_2, po, k, c):
	RR1(po, V_2, c)
	k = RR2(k, po, V_2, G, c)
	return k
	
	#apply RRL01 RRL02 and RRlarge exhaustivaly 
 
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
	branching_algorithm(output, k, V_2, c)
	z = 1


#main 
def main():
	if len(sys.argv) == 0: 
		print("No inputs")
		return
	
	#input = (G, V_1, V_2)
	input = helper.readInput(sys.argv[1])
	V_2 = input[2]

	k_max = 1000 #<=== need to fix this once validated branching 
	po = {}

	minimise(k_max, Algorithm1, input, po)
	out = helper.writeOutput(V_2, po)
	for v in out:
		print(v)

#execute
main()


#Graph representation
graph = {}
#dictionary 
#key : vertex_id v
#values : array of vertex_id u such that there exists an edge v,u in the graph 

#Linear Ordering 
#list of vertex_ids 
#this is generated at the end
lo = []

#Set of Partial Orderings
#dictionary 
#key : vertex_id v 
#value : array of vertex_id u such that v < u in the ordering. 
po = {}

#List storing Linear ordering of V_1
V_1 = []

#List storing vertices of V_2
V_2 = []

def readInput():
	#function to read in stdin and populate graph object
	#graph object: adjacency list 
	#Dictionary, key : vertex, value List<vertex> 
	print("Not Implemented")

def graph_addVertex():
	#add vertex key to dict
	print("Not Implemented")

def graph_addEdge(): 
	#add vertex v1 to dict[v2]
	#add vertex v2 to dict[v1]
	print("Not Implemented")

def graph_deleteVertex():
	#delete key v1
	#delete v1 for all v2 such that dict[v2].contains(v1)
	print("Not Implemented")

def graph_deleteEdge():
	#dict[v1].remove(v2)
	#dict[v2].remove(v1)
	print("Not Implemented")

def graph_getClosedNeighbourhood(v):
	print("Not Implemented")

def execKernal():
	#to execute our Simplification/Halting rules here. 
	print("Not Implemented")

def execAlgorithm():
	print("Not Implemented")

def execAlgorithm1():
	print("Not Implemented")

def execAlgorithm2():
	print("Not Implemented")

def writeOutput(): 
	print("Not Implemented")
	#set of orderings in V_2 and generate linear ordering to output

#computes the number of crossings between {a,b} in V_2 assuming a < b
def getCrossings(a,b):
	print("Not Implemented")
	return 0

#Simplification Rules
def RR1():
	#any pair of vertices {a.b} in V_2 that form a 0/j pattern,
	#commit a < b to the Poset. 
	n = len(V_2)
	for a in range(V_2):
		for b in range (a, V_2):
			if(a != b):
				c_ab = getCrossings(V_2[a],V_2[b])
				c_ba = getCrossings(V_2[b],V_2[a])

				if((c_ab == 0) and (c_ba > 0)): # commit a < b
					po[a].insert(b)
				elif((c_ba == 0) and (c_ab > 0)): # commit b < a
					po[b].insert(a)	

def RR2(k):
	#any pair of vertices {a,b} in V_2 such that N(a)\{a} = N(b)\{b}
	#commit a < b to Poset and do parameter accounting k = k - c_ab
	
	n = len(V_2)
	for a in range(V_2):
		for b in range (a, V_2):
			if(a != b):
				if graph_getClosedNeighbourhood(V_2[a]).remove(V_2[a]) == graph_getClosedNeighbourhood(V_2[b]).remove(V_2[b]):
					po[a].insert(b)
					k = k - getCrossings(V_2[a], V_2[b])

def RRlarge():
	print("Not Implemented")

def RRL01():
	print("Not Implemented")

def RRL02():
	print("Not Implemented")

#takes in empty partial ordering, callback function that is the branching algorithm. 
#executes branching algorithm in a binary search  manner to find k that is minimal. 
def minimise(po, k_max, cb = None):

	#variables 
	#po : List Partial Ordering to be populated 
	#max_k : maximal bound for binary search (that is, the maximal number 
	#			of crossings for bipartite graph G)
	#cb	: callback function to run binary search on (that is, the branching algo we execute)

	po = {} 

	#execute binary search to find minimal k. 
	left = 0
	right = k_max
	if cb:
		while left < right:
			mid = left + (right - left + 1) // 2  # Adding 1 to ensure rounding up
			if cb(mid) == False:
				left = mid
			else:
				right = mid - 1

		#left is maximal value that returns false
		return left + 1
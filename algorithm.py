from graphlib import TopologicalSorter

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

def readInput(fileName):
    f = open(fileName, "r")
    strong = f.read()
    lines = strong.split('\n')[:-1]
    removelist = []
    for i in lines:
        if i[0] == 'c':
            removelist.append(i)
    for rem in removelist:
        lines.remove(rem)
    dimensions = lines[0].split(' ')
    print(dimensions)
    graph = {}
    for x in range(int(dimensions[2])):
        graph[str(x + 1)] = []
    for edge in lines[1:]:
        binglet = edge.split(' ')
    #print(binglet)
        graph[binglet[0]].append(binglet[1])
    return graph
    #function to read in stdin and populate graph object
    #graph object: adjacency list 
    #Dictionary, key : vertex, value List<vertex> 
    #print("Not Implemented")

def graph_addVertex():
    #add vertex key to dict
    print("Not Implemented")

def graph_addEdge(): 
    #add vertex v1 to dict[v2]
    #add vertex v2 to dict[v1]
    print("Not Implemented")

def graph_deleteVertex(graph, vertex):
    if vertex in graph.keys():
        del graph[vertex]
    else:
        for key in graph.keys():
            if vertex in graph[key]:
                graph[key].remove(vertex)
    return(graph)
    #delete key v1
    #delete v1 for all v2 such that dict[v2].contains(v1)
    #print("Not Implemented")

def graph_deleteEdge(graph, start, end):
    if start in graph.keys():
        graph[start].remove(end)
    else:
        graph[end].remove(start)
    return(graph)
    #dict[v1].remove(v2)
    #dict[v2].remove(v1)
    #print("Not Implemented")

def graph_getClosedNeighbourhood(v):
    nbhd = []
    if v in graph.keys():
        nbhd = v
    else:
        for key in graph.keys():
            if v in graph[key]:
                nbhd.append(v)
    return(nbhd)
    #print("Not Implemented")

def execKernal():
    #to execute our Simplification/Halting rules here. 
    print("Not Implemented")

def execAlgorithm():
    print("Not Implemented")

def execAlgorithm1():
    print("Not Implemented")

def execAlgorithm2():
    print("Not Implemented")

def writeOutput(V_2_set, partial_order): 
	"""Set of orderings in V_2 and generate linear ordering to output."""
	"""V_2: the V_2 vertexes set, po: the partial order relation"""
	# Add the remaining keys
	for p1 in V_2_set:
		if not (p1 in partial_order.keys()):
			partial_order[p1] = {}

	# Finding a linear extension from partial order is equivalent to topological sort
    # https://en.wikipedia.org/wiki/Topological_sorting#Relation_to_partial_orders
	linear_order = list(TopologicalSorter(partial_order).static_order())

	# We need to reverse it because the default relation is >, but ours are <
	linear_order.reverse()
	return linear_order

#gets the number of crossings between {a,b} in V_2 assuming a < b
def getCrossings(a, b, c):
    return c[a][b]

#crossings are computed and stored in a dictionary of dictionaries
#key :vertex A 
#value : dictionary with key : vertex B, value : num crossings.
def computeAllCrossings(c, G, V_2, V_1):
    n = len(V_2)
    #init 2d array storing crossings
    #c[a][b] indicates the number of crossings for c_ab (ie assuming a<b in Poset)
    for a in range(n):
        c[V_2[a]] = {}
        for b in range(n):
            if(a == b):
                c[V_2[a]][V_2[b]]= -1
            else:
                c[V_2[a]][V_2[b]]= 0
    
    for a1 in range(n): #vertex in V_2
        for b1 in range (a1, n): #vertex in V_2
            if (a1 == b1):
                continue
            for a2 in G[V_2[a1]]: #vertex in V_1 that has edge incident to a1 in V_2
                for b2 in G[V_2[b1]]: #vertex in V_1 that has edge incident to b1 in V_2
                    a1_i = a1
                    b1_i = b1
                    a2_i = V_1.index(a2)
                    b2_i = V_1.index(b2)
                    if(a2_i == b2_i):
                        continue
                    if (a1_i < b1_i) and (a2_i > b2_i):
                        c[V_2[a1_i]][V_2[b1_i]]+=1
                    elif(a1_i < b1_i) and (a2_i < b2_i):
                        c[V_2[b1_i]][V_2[a1_i]]+=1 #swapping them would force a crossing
                    elif(b1_i < a1_i) and (b2_i > a2_i):
                        c[V_2[b1_i]][V_2[a1_i]]+=1
                    elif(b1_i < a1_i) and (b2_i < a2_i):
                        c[V_2[a1_i]][V_2[b1_i]]+=1 #swapping them would force a crossing    
            

#Simplification Rules
def RR1():
    #any pair of vertices {a.b} in V_2 that form a 0/j pattern,
    #commit a < b to the Poset. 
    n = len(V_2)
    for a in range(n):
        for b in range (a, n):
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
    for a in range(n):
        for b in range (a, n):
            if(a != b):
                if graph_getClosedNeighbourhood(V_2[a]).remove(V_2[a]) == graph_getClosedNeighbourhood(V_2[b]).remove(V_2[b]):
                    po[a].insert(b)
                    k = k - getCrossings(V_2[a], V_2[b])

#takes in empty partial ordering, callback function that is the branching algorithm. 
#executes branching algorithm in a binary search  manner to find k that is minimal. 
def minimise(po, k_max, cb = None):

    #variables 
    #po : List Partial Ordering to be populated 
    #max_k : maximal bound for binary search (that is, the maximal number 
    #            of crossings for bipartite graph G)
    #cb    : callback function to run binary search on (that is, the branching algo we execute)

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
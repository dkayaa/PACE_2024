from graphlib import TopologicalSorter

#Graph representation
#graph = {}
#dictionary 
#key : vertex_id v
#values : array of vertex_id u such that there exists an edge v,u in the graph 

#Linear Ordering 
#list of vertex_ids 
#this is generated at the end
#lo = []

#Set of Partial Orderings
#dictionary 
#key : vertex_id v 
#value : array of vertex_id u such that v < u in the ordering. 
#po = {}

#List storing Linear ordering of V_1
#V_1 = []

#List storing vertices of V_2
#V_2 = []

def readInput(fileName):
	f = open(fileName, "r")
	strong = f.read()
	#print(strong)
	lines = strong.split('\n')[:-1]
	removelist = []
	for i in lines:
		if i[0] == 'c':
			removelist.append(i)
	for rem in removelist:
		lines.remove(rem)
	dimensions = lines[0].split(' ')
	#print(dimensions)
	graph = {}
	V_2 = []
	V_1 = []
	Isolated = []
	#Deniz added this to calculate V_2
	#end
	for x in range(int(dimensions[2])):
		#graph[(x + 1)] = []
		#deniz added this
		V_1.append((x+1))
	for edge in lines[1:]:
		binglet = edge.split(' ')
	#print(binglet)
		
		#graph[int(binglet[0])].append(int(binglet[1]))
		
		if int(binglet[1]) not in graph.keys():
			graph[int(binglet[1])] = []
		graph[int(binglet[1])].append(int(binglet[0]))
	
	
	for x in range(int(dimensions[2]) + 1, int(dimensions[3]) + int(dimensions[2]) + 1):
		if x in graph.keys():
			V_2.append(x)
		else:
			Isolated.append(x)
	i = 0
	for x in graph.keys():
		#print(x, len(graph[x]))
		i += len(graph[x])
	return (graph, V_1, V_2, Isolated)
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

def graph_getClosedNeighbourhood(v, graph):
	nbhd = []
	if v in graph.keys():
		nbhd = graph[v]
		nbhd.append(v)
	else:
		for key in graph.keys():
			if v in graph[key]:
				nbhd.append(v)
	return(nbhd)
	#print("Not Implemented")

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
	if a == b:
		return 0
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
	total = 0
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
		total += min(c[V_2[b1]][V_2[a1]], c[V_2[a1]][V_2[b1]]) 
	return total
			
def insertPartialOrdering(po, a, b, icp = None):
	if a not in po.keys():
		po[a] = []
	if b not in po[a]:
		po[a].append(b)
		if icp:
			icp[a].remove(b)
			icp[b].remove(a)

def commitPartialOrdering(po, a, b, k, c, V_2, icp):
	#commits to partial order and does parameter accounting. 
	#parameter accounting
	#committing a < b to Poset. but b < a
	#reduce k by c_ab but also by c_cd for each pair {c,d} that  is 
	#committed due to transitivity 
	#po[a].append(b)
	if a == b:
		return k
	
	if a in po[b]:
		return -1 

	if b in po[a]:
		return k

	#first calculate k = k - c_ab
	k = k - getCrossings(a, b, c)
	insertPartialOrdering(po, a, b, icp)
	if k < 0:
		return k
	#for any x such that b < x. commit a < x and do param accounting
	for x in po[b]:
		# k = k - getCrossings(a, x, c)
		#insertPartialOrdering(po, a, x)
		#if isTransitive(po, a, x, V_2):
		if x not in po[a]:
			k = commitPartialOrdering(po,a, x, k, c, V_2, icp)
		if k < 0:
			return k
	
	#for any y such that y < a. commit y < b and do param accounting 
	for y in po.keys():
		if y == a:
			continue
		if a in po[y]:
			#k = k - getCrossings(y, b, c)
			#insertPartialOrdering(po, y, b)
			#if isTransitive(po, y, b, V_2):
			k = commitPartialOrdering(po, y, b, k, c, V_2, icp)
			if k < 0:
				return k
	return k

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

# Checks if two vertices are comparable 
def incomparable(po, a, b):
	if (b not in po[a]) and (a not in po[b]):
		return True
	return False

# Checks if two vertices are dependent on any vertices
def isDependent(po, a, b, V_2):
	for vertex in V_2:
		if a == vertex or b == vertex:
			continue
		if incomparable(po, a, vertex) or incomparable(po, b, vertex):
			return True
	return False

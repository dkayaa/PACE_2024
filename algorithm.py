
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

def execKernal():
	#to execute our Simplification/Halting rules here. 
	print("Not Implemented")

def execAlgorithm1():
	print("Not Implemented")

def execAlgorithm2():
	print("Not Implemented")

def writeOutput(): 
	print("Not Implemented")
	#set of orderings in V_2 and generate linear ordering to output

#Simplification Rules
def RR1():
	print("Not Implemented")

def RR2():
	print("Not Implemented")

def RRlarge():
	print("Not Implemented")

def RRL01():
	print("Not Implemented")

def RRL02():
	print("Not Implemented")

def minimise():
	#execute binary search on 

#Main
readInput()
execKernal()
execAlgorithm1()
execAlgorithm2()

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
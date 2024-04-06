from algorithm import getCrossings
import copy
def branching_algorithm(po, k, V_2, c):
	prevK = -1
	prevSize = -1
	while prevK != k or prevSize != len(V_2):
		
		prevK = k
		prevSize = len(V_2)
		
		# RRLO1
		for a in range(len(V_2)):
			comparable = True
			for b in range(len(V_2)):
				if a == b:
					continue
				if b not in po[V_2[a]] and a not in po[V_2[b]]:
					comparable = False
					break
			if comparable:
				V_2.pop(a)
				po.pop(V_2[a], None)
				for c in range(V_2):
					if a == c:
						continue
					po[V_2[c]].remove(V_2[a])
		
		# RRL02
		for a in range(len(V_2)):
			for b in range(a + 1, len(V_2)):
				if incomparable(po, V_2[a], V_2[b]) and not isDependent(po, V_2[a], V_2[b], V_2):
					i = getCrossings(V_2[a], V_2[b], c)
					j = getCrossings(V_2[b], V_2[a], c)
					if (i < j):
						po[V_2[a]].append(V_2[b])
						k -= i
					else:
						po[V_2[b]].append(V_2[a])
						k -= j
		
		# RRlarge
		for a in range(len(V_2)):
			for b in range(a + 1, len(V_2)):
				if not incomparable(po,V_2[a],V_2[b]):
					continue
				i = getCrossings(V_2[a], V_2[b], c)
				j = getCrossings(V_2[b], V_2[a], c)
				if i > k and j > k:
					return False
				elif i > k:
					k -= j
					po[V_2[b]].append(V_2[a])
				elif j > k:
					k -= i
					po[V_2[a]].append(V_2[b])
	if (k < 0):
		return False

	for v_1 in range(len(V_2)):
		for v_2 in range(v_1 + 1, len(V_2)):
			i = getCrossings(V_2[v_1], V_2[v_2], c)
			j = getCrossings(V_2[v_2], V_2[v_1], c)
			isIncomparable = incomparable(po, V_2[v_1], V_2[v_2])
			if not isIncomparable:
				continue
			if i + j >= 4:
				po1 = copy.deepcopy(po)
				po1[V_2[v_1]].append(V_2[v_2])
				po[V_2[v_2]].append(V_2[v_1])
				return branching_algorithm(po, k - i,V_2, c) or branching_algorithm(po1, k-j,V_2, c)
			elif (i == 1 and j == 2) or (i == 2 and j == 1) and isDependent(po, V_2[v_1],V_2[v_2]):
				po1 = copy.deepcopy(po)
				po1[V_2[v_1]].append(V_2[v_2])
				po[V_2[v_2]].append(V_2[v_1])
				return branching_algorithm(po, k-i, V_2, c) or branching_algorithm(po1, k-j, V_2, c)
			elif i == 1 and j == 1:
				po[V_2[v_1]].append(V_2[v_2])
				return branching_algorithm(po, k-1, V_2, c)           
	return True

# Checks if two vertices are comparable 
def incomparable(po, a, b):
	if b not in po[a] and a not in po[b]:
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

    
    



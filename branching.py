from helper import getCrossings, incomparable, isDependent
import copy	
import helper

#Simplification Rules
def RR1(po, V_2, c, k, icp):
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
					k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k , c, V_2, icp)
					#po[V_2[a]].append(V_2[b])
				elif((c_ba == 0) and (c_ab > 0)): # commit b < a
					k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c, V_2, icp)
					#po[V_2[b]].append(V_2[a])
				if c_ab == 0 and c_ba == 0:
					k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c, V_2, icp)
				if k < 0:
					return k

	 		
	return k

def RR2(k, po, V_2, G, c, icp):
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
					k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c, V_2, icp)
				if k < 0:
					return k
	return k

def RR3(k, po, V_2, c, icp):
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
				k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c, V_2, icp)	
			if k < 0:
				return k
	return k

def RRL01(po, V_2):
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
				for e in range(V_2):
					if a == e:
						continue
					po[V_2[e]].remove(V_2[a])

def RRL02(po, V_2, c, k, icp):
	for a in range(len(V_2)):
		for b in range(a + 1, len(V_2)):
			if incomparable(po, V_2[a], V_2[b]) and not isDependent(po, V_2[a], V_2[b], V_2):
				i = getCrossings(V_2[a], V_2[b], c)
				j = getCrossings(V_2[b], V_2[a], c)
				if (i <= j):
					k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c, V_2, icp)
					#po[V_2[a]].append(V_2[b])
				else:
					#po[V_2[b]].append(V_2[a])
					k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c, V_2, icp)
				if k < 0:
					return k
	return k

def RRlarge(po, V_2, c, k, icp):
	for a in range(len(V_2)):
		for b in range(a + 1, len(V_2)):
			if not incomparable(po,V_2[a],V_2[b]):
				continue
			i = getCrossings(V_2[a], V_2[b], c) #cab
			j = getCrossings(V_2[b], V_2[a], c) #cba
			if i > k and j > k:
				return -1
			elif i > k:
				#po[V_2[b]].append(V_2[a])
				k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c, V_2, icp)
			elif j > k:
				#po[V_2[a]].append(V_2[b])
				k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c, V_2, icp)
	return k


def Kernalize(G, V_2, po, k, c, icp):
	#apply exhaustively
	prevK = -1
	while prevK != k: 
		prevK = k
		#print("got here")
		k = RR1(po, V_2, c, k, icp)
		if k < 0:
			return k
		#print("got here")
		k = RR2(k, po, V_2, G, c, icp)
		if k < 0:
			return k

	#apply RRL01 RRL02 and RRlarge exhaustivaly 
	prevK = -1
	while prevK != k:
		prevK = k
		RRL01(po, V_2)
		k = RRL02(po, V_2, c, k, icp)
		if k < 0:
			return k
		k = RRlarge(po, V_2, c, k, icp)
		if k < 0:
			return k
	return k

def branching_algorithm(po, k, V_2, c, icp):
	prevK = -1
	prevSize = -1
	po_original = copy.deepcopy(po)
	V_2_original = copy.deepcopy(V_2)
	icp_original = copy.deepcopy(icp)
	
	while prevK != k or prevSize != len(V_2):
		
		prevK = k
		prevSize = len(V_2)
		
		# RRLO1
		RRL01(po, V_2)
		
		# RRL02
		k = RRL02(po, V_2, c, k, icp)
		
		
		# RRlarge
		k = RRlarge(po, V_2, c, k, icp)
		
		if k < 0: 
			po.clear()
			po.update(po_original)
			V_2.clear()
			V_2 += V_2_original
			icp.clear()
			icp.update(icp_original)
			return False
		

	if (k < 0):
		po.clear()
		po.update(po_original)
		V_2.clear()
		V_2 += V_2_original
		icp.clear()
		icp.update(icp_original)
		return False

	po2 = copy.deepcopy(po)
	po1 = copy.deepcopy(po)
	icp2 = copy.deepcopy(icp)
	icp1 = copy.deepcopy(icp)
	# finished = False

	# for v_1 in range(len(V_2)):
	# 	for v_2 in range(v_1 + 1, len(V_2)):
	# 		finished = incomparable(po, V_2[v_1], V_2[v_2])
	# 		if finished:
	# 			break
	# 	if finished:
	# 		break
	# if not finished:
	# 	return True
	
	#for v_1 in range(len(V_2)):
	#	for v_2 in range(v_1 + 1, len(V_2)):
	for v_1 in icp.keys():
		for v_2 in icp[v_1]:
			#i = getCrossings(V_2[v_1], V_2[v_2], c)
			#j = getCrossings(V_2[v_2], V_2[v_1], c)
			i = getCrossings(v_1, v_2, c)
			j = getCrossings(v_2, v_1, c)
			isIncomparable = incomparable(po, v_1, v_2)
			if not isIncomparable:
				continue
			if ((i + j) >= 4) and isIncomparable:
				#k_i = helper.commitPartialOrdering(po1, V_2[v_1], V_2[v_2], k, c, V_2, icp1)
				#k_j = helper.commitPartialOrdering(po2, V_2[v_2], V_2[v_1], k, c, V_2, icp2)
				k_i = helper.commitPartialOrdering(po1, v_1, v_2, k, c, V_2, icp1)
				k_j = helper.commitPartialOrdering(po2, v_2, v_1, k, c, V_2, icp2)
				#Sanks Original Return Clause
				#return branching_algorithm(po, k - j,V_2, c) or branching_algorithm(po1, k-i,V_2, c)
				if k_j >= 0:
					r1 = branching_algorithm(po2, k_j,V_2, c, icp)
					if r1: 
						po.clear()
						po.update(po2)
						icp.clear()
						icp.update(icp2)
						return r1
				if k_i >= 0 :
					r2 = branching_algorithm(po1, k_i,V_2, c, icp)
					if r2:
						#po = copy.deepcopy(po1)
						po.clear()
						po.update(po1)
						icp.clear()
						icp.update(icp1)
						return r2
				po.clear()
				po.update(po_original)
				V_2.clear()
				V_2 += V_2_original
				icp.clear()
				icp.update(icp_original)
				return False
	#for v_1 in range(len(V_2)):
	#	for v_2 in range(v_1 + 1, len(V_2)):
	for v_1 in icp.keys():
		for v_2 in icp[v_1]:
			#i = getCrossings(V_2[v_1], V_2[v_2], c)
			#j = getCrossings(V_2[v_2], V_2[v_1], c)
			#isIncomparable = incomparable(po, V_2[v_1], V_2[v_2])
			i = getCrossings(v_1, v_2, c)
			j = getCrossings(v_2, v_1, c)
			isIncomparable = incomparable(po, v_1, v_2)
			if not isIncomparable:
				continue
			if (i == 1 and j == 2) or (i == 2 and j == 1) and isDependent(po, v_1, v_2, V_2):
				k_i = helper.commitPartialOrdering(po1, v_1, v_2, k, c, V_2, icp1)
				k_j = helper.commitPartialOrdering(po2, v_2, v_1, k, c, V_2, icp2)
				# po is if we commit v_2 < v_1 , c21 = j
				#return branching_algorithm(po, k-i, V_2, c) or branching_algorithm(po1, k-j, V_2, c)
				#return branching_algorithm(po, k-j, V_2, c) or branching_algorithm(po1, k-i, V_2, c)
				if k_j >= 0:
					r1 = branching_algorithm(po2, k_j,V_2, c, icp)
					if r1: 
						po.clear()
						po.update(po2)
						icp.clear()
						icp.update(icp2)
						return r1
				if k_i >= 0:
					r2 = branching_algorithm(po1, k_i,V_2, c, icp)
					if r2:
						#po = copy.deepcopy(po1)
						po.clear()
						po.update(po1)
						icp.clear()
						icp.update(icp1)
						return r2
				po.clear()
				po.update(po_original)
				V_2.clear()
				V_2 += V_2_original
				icp.clear()
				icp.update(icp_original)
				return False
	#for v_1 in range(len(V_2)):
	#	for v_2 in range(v_1 + 1, len(V_2)):
	for v_1 in icp.keys():
		for v_2 in icp[v_1]:
			#i = getCrossings(V_2[v_1], V_2[v_2], c)
			#j = getCrossings(V_2[v_2], V_2[v_1], c)
			#isIncomparable = incomparable(po, V_2[v_1], V_2[v_2])
			i = getCrossings(v_1, v_2, c)
			j = getCrossings(v_2, v_1, c)
			isIncomparable = incomparable(po, v_1, v_2)
			if not isIncomparable:
				continue
			if i == 1 and j == 1:
				#k = helper.commitPartialOrdering(po, V_2[v_1], V_2[v_2], k, c, V_2, icp)
				k = helper.commitPartialOrdering(po, v_1, v_2, k, c, V_2, icp)
				if k >= 0:
					r1 = branching_algorithm(po, k, V_2, c, icp)
					if r1: 
						return r1
				po.clear()
				po.update(po_original)
				V_2.clear()
				V_2 += V_2_original
				icp.clear()
				icp.update(icp_original)
				return False
					
	
	# po.clear()
	# po.update(po_original)
	# V_2.clear()
	# V_2 += V_2_original
	return True

def Algorithm1 (k, input, output):
	#unpack inputs
	G = input[0]
	V_1 = input[1]
	V_2 = input[2]
	c = input[3]
	icp = input[4]

	for key in G.keys():
		output[key] = []
	
	k = Kernalize(G, V_2, output, k, c, icp)
	if k < 0:
		return False
	#apply RR3 exhaustively
	prevK = -1
	while prevK != k:
		prevK = k
		k = RR3(k, output, V_2, c, icp)
		if k < 0:
			return False

	r = branching_algorithm(output, k, V_2, c, icp)
	return r
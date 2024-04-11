from helper import getCrossings, incomparable, isDependent
import copy	
import helper

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

def RRL02(po, V_2, c, k):
	for a in range(len(V_2)):
		for b in range(a + 1, len(V_2)):
			if incomparable(po, V_2[a], V_2[b]) and not isDependent(po, V_2[a], V_2[b], V_2):
				i = getCrossings(V_2[a], V_2[b], c)
				j = getCrossings(V_2[b], V_2[a], c)
				if (i <= j):
					k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c, V_2)
					#po[V_2[a]].append(V_2[b])
				else:
					#po[V_2[b]].append(V_2[a])
					k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c, V_2)
				if k < 0:
					return k
	return k

def RRlarge(po, V_2, c, k):
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
				k = helper.commitPartialOrdering(po, V_2[b], V_2[a], k, c, V_2)
			elif j > k:
				#po[V_2[a]].append(V_2[b])
				k = helper.commitPartialOrdering(po, V_2[a], V_2[b], k, c, V_2)
	return k

def branching_algorithm(po, k, V_2, c):
	prevK = -1
	prevSize = -1
	po_original = copy.deepcopy(po)
	V_2_original = copy.deepcopy(V_2)
	
	while prevK != k or prevSize != len(V_2):
		
		prevK = k
		prevSize = len(V_2)
		
		# RRLO1
		RRL01(po, V_2)
		
		# RRL02
		k = RRL02(po, V_2, c, k)
		
		
		# RRlarge
		k = RRlarge(po, V_2, c, k)
		
		if k < 0: 
			return False
		

	if (k < 0):
		po.clear()
		po.update(po_original)
		return False

	po2 = copy.deepcopy(po)
	po1 = copy.deepcopy(po)
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
	
	case_found = False
	for v_1 in range(len(V_2)):
		for v_2 in range(v_1 + 1, len(V_2)):
			i = getCrossings(V_2[v_1], V_2[v_2], c)
			j = getCrossings(V_2[v_2], V_2[v_1], c)
			isIncomparable = incomparable(po, V_2[v_1], V_2[v_2])
			if not isIncomparable:
				continue
			if ((i + j) >= 4) and isIncomparable:
				k_i = helper.commitPartialOrdering(po1, V_2[v_1], V_2[v_2], k, c, V_2)
				k_j = helper.commitPartialOrdering(po2, V_2[v_2], V_2[v_1], k, c, V_2)
				#Sanks Original Return Clause
				#return branching_algorithm(po, k - j,V_2, c) or branching_algorithm(po1, k-i,V_2, c)
				if k_j >= 0:
					r1 = branching_algorithm(po2, k_j,V_2, c)
					if r1: 
						po.clear()
						po.update(po2)
						return r1
				if k_i >= 0 :
					r2 = branching_algorithm(po1, k_i,V_2, c)
					if r2:
						#po = copy.deepcopy(po1)
						po.clear()
						po.update(po1)
						return r2
				po.clear()
				po.update(po_original)
				return False
	for v_1 in range(len(V_2)):
		for v_2 in range(v_1 + 1, len(V_2)):
			i = getCrossings(V_2[v_1], V_2[v_2], c)
			j = getCrossings(V_2[v_2], V_2[v_1], c)
			isIncomparable = incomparable(po, V_2[v_1], V_2[v_2])
			if not isIncomparable:
				continue
			if (i == 1 and j == 2) or (i == 2 and j == 1) and isDependent(po, V_2[v_1],V_2[v_2], V_2):
				k_i = helper.commitPartialOrdering(po1, V_2[v_1], V_2[v_2], k, c, V_2)
				k_j = helper.commitPartialOrdering(po2, V_2[v_2], V_2[v_1], k, c, V_2)
				# po is if we commit v_2 < v_1 , c21 = j
				#return branching_algorithm(po, k-i, V_2, c) or branching_algorithm(po1, k-j, V_2, c)
				#return branching_algorithm(po, k-j, V_2, c) or branching_algorithm(po1, k-i, V_2, c)
				if k_j >= 0:
					r1 = branching_algorithm(po2, k_j,V_2, c)
					if r1: 
						po.clear()
						po.update(po2)
						return r1
				if k_i >= 0:
					r2 = branching_algorithm(po1, k_i,V_2, c)
					if r2:
						#po = copy.deepcopy(po1)
						po.clear()
						po.update(po1)
						return r2
				po.clear()
				po.update(po_original)
				return False
	for v_1 in range(len(V_2)):
		for v_2 in range(v_1 + 1, len(V_2)):
			i = getCrossings(V_2[v_1], V_2[v_2], c)
			j = getCrossings(V_2[v_2], V_2[v_1], c)
			isIncomparable = incomparable(po, V_2[v_1], V_2[v_2])
			if not isIncomparable:
				continue
			if i == 1 and j == 1:
				k = helper.commitPartialOrdering(po, V_2[v_1], V_2[v_2], k, c, V_2)
				if k >= 0:
					r1 = branching_algorithm(po, k, V_2, c)
					if r1: 
						return r1
				po.clear()
				po.update(po_original)
				return False
					
	
	# po.clear()
	# po.update(po_original)
	# V_2.clear()
	# V_2 += V_2_original
	return True



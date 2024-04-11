import helper
import copy 
from branching import incomparable

def BruteForce (k, input, output):
	#unpack inputs
	G = input[0]
	V_1 = input[1]
	V_2 = input[2]
	c = {}
	for key in G.keys():
		output[key] = []
	helper.computeAllCrossings(c, G, V_2, V_1)

	r = BruteForceRecursing(output, k, V_2, c)
	return r

def BruteForceRecursing(po, k, V_2, c):
	
	if k < 0:
		return False

	n = len(V_2)

	inComparable = False
	for a in range(n):
		for b in range(a+1, n):
			v_a = V_2[a]
			v_b = V_2[b]
			if (incomparable(po, v_a, v_b)):
				inComparable = True
				break
	
	#if everything is comparable 
	if not inComparable:
		return True
	
	#pick arbitrary pair of vertices a, b in V_2 
	#recurse on a < b 
	# else 
	#recurse on a > b

	for a in range(n):
		for b in range(a+1, n):
			if(a == b):
				continue
			v_a = V_2[a]
			v_b = V_2[b]
			if (incomparable(po, v_a, v_b)):
				po_a = copy.deepcopy(po)
				ka = helper.commitPartialOrdering(po_a, v_a, v_b, k, c)
				if BruteForceRecursing(po_a, ka, V_2, c):
					po.clear()
					po.update(po_a)
					return True
				po_a.clear()

				po_b = copy.deepcopy(po)
				kb = helper.commitPartialOrdering(po_b, v_b, v_a, k, c)
				if BruteForceRecursing(po_b, kb, V_2, c):
					po.clear()
					po.update(po_b)
					return True 
				po_b.clear()
							
	return True
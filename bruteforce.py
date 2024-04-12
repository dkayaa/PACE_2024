import helper
import copy 
from helper import incomparable

def BruteForce (k, input, output):
	#unpack inputs
	G = input[0]
	V_1 = input[1]
	V_2 = input[2]
	c = input[3]
	for key in G.keys():
		output[key] = []

	icp = input[4]
	r = BruteForceRecursing(output, k, V_2, c, icp)
	return r

def BruteForceRecursing(po, k, V_2, c, icp):
	
	if k < 0:
		return False

	n = len(V_2)

	inComparable = False
	for a in range(n):
		for b in range(a+1, n):
			if a == b:
				continue
			v_a = V_2[a]
			v_b = V_2[b]
			if (incomparable(po, v_a, v_b)):
				inComparable = True
				break
		if inComparable:
			break
	
	#if everything is comparable 
	if not inComparable:
		return True
	
	
	po_a = copy.deepcopy(po)
	icp_a = copy.deepcopy(icp)
	ka = helper.commitPartialOrdering(po_a, v_a, v_b, k, c, V_2, icp_a)
	if ka >= 0:
			if BruteForceRecursing(po_a, ka, V_2, c, icp):
				po.clear()
				po.update(po_a)
				icp.clear()
				icp.update(icp_a)
				return True
	po_a.clear()
	icp_a.clear()

	po_b = copy.deepcopy(po)
	icp_b = copy.deepcopy(icp)
	kb = helper.commitPartialOrdering(po_b, v_b, v_a, k, c, V_2, icp_b)
	if kb >= 0:
		if BruteForceRecursing(po_b, kb, V_2, c, icp):
			po.clear()
			po.update(po_b)
			icp.clear()
			icp.update(icp_b)
			return True 
	po_b.clear()
	icp_b.clear()

	#pick arbitrary pair of vertices a, b in V_2 
	#recurse on a < b 
	# else 
	#recurse on a > b
	return False

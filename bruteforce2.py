import helper
import copy 
from helper import incomparable

def BruteForce2(k, input, order):
	#unpack inputs
	G = input[0]
	V_1 = input[1]
	V_2 = input[2]
	c = input[3]
	order.append(V_2[0])
	index = 1
	r = BruteForceRecursing2(order, k, V_2, c, index)
	return r

def BruteForceRecursing2(order, k, V_2, c, index):
	if k < 0:
		return False

	if len(order) == len(V_2):
		return True

	size = len(order)
	for i in range(size + 1):
		order.insert(i, V_2[index])
		cost = comupteAllCosts(order, i, c)
		if k - cost < 0:
			order.pop(i)
			continue
		
		r = BruteForceRecursing2(order, k - cost, V_2, c, index + 1)
		if r:
			return r
		order.pop(i)
	return False


def comupteAllCosts(po, index, c):
	total = 0
	new = po[index]
	for i, element in enumerate(po):
		if index == i:
			continue
		if index < i:
			total += helper.getCrossings(new, element, c)
		else:
			total += helper.getCrossings(element, new, c)
	return total
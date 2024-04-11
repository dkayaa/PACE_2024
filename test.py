#some unit tests for methods
#using unittest test package. 

import unittest 
import algorithm
import branching
import helper

def myfunc(k, i, o):
	i.clear()
	if k > 5:
		o[1] = []
		o[1].append(1)
		return True
	return False

#test cases here
#-------------------------------------#
class Test(unittest.TestCase):

	def test_minimise_1(self):
		c = lambda k, i , o : k >= 15
		val = algorithm.minimise(20, c);
		self.assertEqual(val, 15, "minimise returned: " + str(val))

	def test_minimise_2(self):
		c = lambda k, i , o : k >= 5
		val = algorithm.minimise(20, c)
		self.assertEqual(val, 5, "minimise returned: " + str(val))

	def test_minimise_3(self):
		o = {}
		i = {10:[10]}
		c = lambda k, i , o : k >= 5
		val = algorithm.minimise(20, c)
		self.assertEqual(val, 5, "minimise returned: " + str(val))
		self.assertEqual(i, {10:[10]}, "input not equal: " + str(o))
		myfunc(val,i,o)
		self.assertEqual(o, {}, "output not equal: " + str(o))


	def test_computeCross2X2Bipartite(self):
		
		c = {}
		V_1 = [1,2]
		V_2 = [3,4]
		G = {}
		G[1] = [4,3]
		G[2] = [3,4]
		G[3] = [2,1]
		G[4] = [1,2]

		helper.computeAllCrossings(c, G, V_2, V_1)
		val = helper.getCrossings(3,4,c)
		self.assertEqual(val, 1, "crossings returned: " + str(val))

	def test_computeCross2XP2(self):
		
		#	(1)	(2)
		#	 |	 |
		#	(3)	(4)

		c = {}
		V_1 = [1,2]
		V_2 = [3,4]
		G = {}
		G[1] = [3]
		G[2] = [4]
		G[3] = [1]
		G[4] = [2]

		helper.computeAllCrossings(c, G, V_2, V_1)
		val = helper.getCrossings(3,4,c)
		self.assertEqual(val, 0, "crossings returned: " + str(val))
		val = helper.getCrossings(4,3,c)
		self.assertEqual(val, 1, "crossings returned: " + str(val))


	def test_computeCross3X3Bipartite(self):
		
		c = {}
		V_1 = [1,2,3]
		V_2 = [4,5,6]
		G = {}
		G[1] = [4,5,6]
		G[2] = [4,5,6]
		G[3] = [4,5,6]
		G[4] = [1,2,3]
		G[5] = [1,2,3]
		G[6] = [1,2,3]

		helper.computeAllCrossings(c, G, V_2, V_1)
		val = helper.getCrossings(4,6,c)
		self.assertEqual(val, 3, "crossings returned: " + str(val)) 
		val = helper.getCrossings(4,5,c)
		self.assertEqual(val, 3, "crossings returned: " + str(val)) 
		val = helper.getCrossings(6,4,c)
		self.assertEqual(val, 3, "crossings returned: " + str(val)) 
		val = helper.getCrossings(5,4,c)
		self.assertEqual(val, 3, "crossings returned: " + str(val)) 
				
	
	def test_branching2X2Bipartite(self):
		c = {}
		pos = {3:[], 4:[]}
		V_1 = [1,2]
		V_2 = [3,4]
		G = {}
		G[1] = [4,3]
		G[2] = [3,4]
		G[3] = [2,1]
		G[4] = [1,2]

		helper.computeAllCrossings(c, G, V_2, V_1)
		
		val = branching.branching_algorithm(pos, 0, V_2, c)
		self.assertEqual(val, False, "The is a " + str(val) + " instance")
		val = branching.branching_algorithm(pos, 1, V_2, c)
		self.assertEqual(val, True, "The is a " + str(val) + " instance")
	
	def test_branching2XP2(self):
		c = {3:{4:0}, 4:{3:1}}
		pos = {3:[], 4:[]}
		V_1 = [1,2]
		V_2 = [3,4]
		G = {}
		G[1] = [3]
		G[2] = [4]
		G[3] = [1]
		G[4] = [2]
		
		val = branching.branching_algorithm(pos, 0, V_2, c)
		self.assertEqual(val, True, "The is a " + str(val) + " instance")
		
	
	
	def test_branching3X3Bipartite(self):
		
		c = {4:{5:3, 6:3}, 5:{4:3, 6:3}, 6:{4:3, 5:3}}
		
		pos = {4:[], 5:[], 6:[]}
		V_1 = [1,2,3]
		V_2 = [4,5,6]
		G = {}
		G[1] = [4,5,6]
		G[2] = [4,5,6]
		G[3] = [4,5,6]
		G[4] = [1,2,3]
		G[5] = [1,2,3]
		G[6] = [1,2,3]
		
		val = branching.branching_algorithm(pos, 8, V_2, c)
		self.assertEqual(val, False, "The is a " + str(val) + " instance")
		val = branching.branching_algorithm(pos, 9, V_2, c)
		self.assertEqual(val, True, "The is a " + str(val) + " instance")

	def test_linearOrder_1(self):
		po = {
			0: {1, 2},
			1: {3, 4},
	  		3: {5}
			}

		V_2 = [0, 1, 2, 3, 4, 5, 6]

		result = helper.writeOutput(V_2, po)
		self.assertEqual(result, [0, 1, 3, 6, 5, 4, 2])


	def test_insertPO1(self):
		po = {}
		helper.insertPartialOrdering(po, 1, 2)
		expected = {1:[2]}
		self.assertEqual(po, expected, "failed: " + str(po))

	def test_insertPO2(self):
		po = {1:[]}
		helper.insertPartialOrdering(po, 1, 2)
		expected = {1:[2]}
		self.assertEqual(po, expected, "failed: " + str(po))

	def test_insertPO3(self):
		po = {1:[2]}
		helper.insertPartialOrdering(po, 1, 2)
		expected = {1:[2]}
		self.assertEqual(po, expected, "failed: " + str(po))

	def test_insertPO4(self):
		po = {2:[10]}
		helper.insertPartialOrdering(po, 1, 2)
		expected = {2:[10], 1:[2]}
		self.assertEqual(po, expected, "failed: " + str(po))

	#if 1 < 2 and commit 3 < 1, then 3 < 2 committed by transitivity
	def test_commitPO1(self):
		c = {1: {2: 0, 3:0}, 2: {1: 0, 3:0}, 3: {1:0, 2:10}}
		po = {1: [2], 2:[], 3:[]}
		k = 0
		k = helper.commitPartialOrdering(po, 3, 1, k, c, [1, 2, 3])
		self.assertEqual(k, -10, "incorrect")

	#if 1 < 2 and commit  2 < 3 then 1 < 3 committed by transitivity
	def test_commitPO2(self):
		c = {1: {2: 0, 3:2}, 2: {1: 0, 3:5}, 3: {1:0, 2:0}}
		po = {1: [2], 2:[], 3:[]}
		k = 0
		k = helper.commitPartialOrdering(po, 2, 3, k, c, [1, 2, 3])
		self.assertEqual(k, -7, "incorrect")
		self.assertEqual(po, {1: [2,3], 2:[3], 3:[]},"incorrect")

	def test_isTransitive1(self):
		c = {1: {2: 0, 3:2}, 2: {1: 0, 3:5}, 3: {1:0, 2:0}}
		po = {1: [3], 2:[], 3:[2]}
		# 1 < 3 and 3 < 2
		# a < c and c < b
		# are {a, b} transitive?
		# exists c such that {a,c} are comp or {b,c} are comp but not both
		r = helper.isTransitive(po, 1, 2, [1, 2, 3])
		self.assertEqual(r, False, "incorrect")	

	def test_isTransitive2(self):
		c = {1: {2: 0, 3:2}, 2: {1: 0, 3:5}, 3: {1:0, 2:0}}
		po = {1: [3], 2:[], 3:[]}
		# 1 < 3 and 3 < 2
		# a < c and c < b
		# are {a, b} transitive?
		# exists c such that {a,c} are comp or {b,c} are comp but not both
		r = helper.isTransitive(po, 1, 2, [1, 2, 3])
		self.assertEqual(r, True, "incorrect")	

#add more here
#-------------------------------------#
	
#execute unittest main method to run unit tests.
unittest.main()
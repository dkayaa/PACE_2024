#some unit tests for methods
#using unittest test package. 

import unittest 
import algorithm
import branching

#test cases here
#-------------------------------------#
class Test(unittest.TestCase):

	def test_minimise_1(self):
		c = lambda k : k >= 15
		val = algorithm.minimise({},20, c);
		self.assertEqual(val, 15, "minimise returned: " + str(val))

	def test_minimise_2(self):
		c = lambda k : k >= 5
		val = algorithm.minimise({},20, c);
		self.assertEqual(val, 5, "minimise returned: " + str(val))

	def test_computeCross2X2Bipartite(self):
		
		c = {}
		V_1 = [1,2]
		V_2 = [3,4]
		G = {}
		G[1] = [4,3]
		G[2] = [3,4]
		G[3] = [2,1]
		G[4] = [1,2]

		algorithm.computeAllCrossings(c, G, V_2, V_1)
		val = algorithm.getCrossings(3,4,c)
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

		algorithm.computeAllCrossings(c, G, V_2, V_1)
		val = algorithm.getCrossings(4,6,c)
		self.assertEqual(val, 3, "crossings returned: " + str(val))

	def test_branching2X2Bipartite(self):
		c = {}
		pos = {0:[], 1:[]}
		V_1 = [1,2]
		V_2 = [3,4]
		G = {}
		G[1] = [4,3]
		G[2] = [3,4]
		G[3] = [2,1]
		G[4] = [1,2]

		algorithm.computeAllCrossings(c, G, V_2, V_1)
		
		val = branching.branching_algorithm(pos, 0, V_2, c)
		self.assertEqual(val, False, "The is a " + str(val) + " instance")
		val = branching.branching_algorithm(pos, 1, V_2, c)
		self.assertEqual(val, True, "The is a " + str(val) + " instance")

	def test_computeCross3X3Bipartite(self):
		
		c = {}
		pos = {0:[], 1:[], 2:[]}
		V_1 = [1,2,3]
		V_2 = [4,5,6]
		G = {}
		G[1] = [4,5,6]
		G[2] = [4,5,6]
		G[3] = [4,5,6]
		G[4] = [1,2,3]
		G[5] = [1,2,3]
		G[6] = [1,2,3]

		algorithm.computeAllCrossings(c, G, V_2, V_1)
		val = branching.branching_algorithm(pos, 8, V_2, c)
		self.assertEqual(val, False, "The is a " + str(val) + " instance")
		val = branching.branching_algorithm(pos, 9, V_2, c)
		self.assertEqual(val, True, "The is a " + str(val) + " instance")


#add more here
#-------------------------------------#
	
#execute unittest main method to run unit tests.
unittest.main()
#some unit tests for methods
#using unittest test package. 

import unittest 
import algorithm
import branching
import helper

#test cases here
#-------------------------------------#
class Test(unittest.TestCase):

	def test_minimise_1(self):
		c = lambda k, i , o : k >= 15
		val = algorithm.minimise(20, c);
		self.assertEqual(val, 15, "minimise returned: " + str(val))

	def test_minimise_2(self):
		c = lambda k, i , o : k >= 5
		val = algorithm.minimise(20, c);
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

#add more here
#-------------------------------------#
	
#execute unittest main method to run unit tests.
unittest.main()
#some unit tests for methods
#using unittest test package. 

import unittest 
import algorithm

#test cases here
#-------------------------------------#
class TestMinimise(unittest.TestCase):

	def test_minimise_1(self):
		c = lambda k : k >= 15
		val = algorithm.minimise({},20, c);
		self.assertEqual(val, 15, "minimise returned: " + str(val))

	def test_minimise_2(self):
		c = lambda k : k >= 5
		val = algorithm.minimise({},20, c);
		self.assertEqual(val, 5, "minimise returned: " + str(val))

#add more here
#-------------------------------------#

#execute unittest main method to run unit tests.
unittest.main()
from ...RleClass import Rle

class TestClass:
	def test_empty_multiplication(self):
		assert Rle()*3 == Rle()
	
	def test_0_multiplication(self):
		assert 0 * Rle([1, 3, 3, 4]) == Rle([0], [4])
	
	def test_example(self):
		assert 2 * Rle([1, 3, 3, 4], [2, 3, 1, 4]) == Rle([2, 6, 8], [2, 4, 4])
	
	def test_commutativity(self):
		assert 2 * Rle([1, 3, 3, 4], [2, 3, 1, 4]) == Rle([1, 3, 3, 4], [2, 3, 1, 4]) * 2


from ...RleClass import Rle
import pytest

class TestClass:
	def test_sub_empty_Rle(self):
		assert Rle() - Rle() == Rle()
	
	def test_different_lengths(self):
		with pytest.raises(AssertionError):
			Rle([1, 2, 3]) - Rle([1, 2])
	
	def test_example(self):
		assert Rle([1, 3, 3, 5, 5, 4]) - Rle([3, 1, 4, 1, 2, 2]) == Rle([-2, 2, -1, 4, 3, 2])


	def test_cummutativity(self):
		assert Rle([1, 3, 3, 5, 5, 4]) - Rle([3, 1, 4, 1, 2, 2]) != Rle([3, 1, 4, 1, 2, 2]) - Rle([1, 3, 3, 5, 5, 4])
	
	def test_compression(self):
		assert Rle([1, 3, 4]) - Rle([1, 3, 4]) == Rle([0], [3])
	


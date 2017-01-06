from ...RleClass import Rle
import pytest

class TestClass:
	def test_adding_empty_rles(self):
		assert Rle() + Rle() == Rle()
	
	def test_different_lengths(self):
		with pytest.raises(AssertionError):
			Rle([1, 2, 3]) + Rle([1, 2])
	
	def test_compression(self):
		assert Rle([1, 3, 3, 5, 5, 4]) + Rle([3, 1, 4, 1, 2, 2]) == Rle([4, 4, 7, 6, 7, 6])


	def test_cummutativity(self):
		assert Rle([1, 3, 3, 5, 5, 4]) + Rle([3, 1, 4, 1, 2, 2]) == Rle([3, 1, 4, 1, 2, 2]) + Rle([1, 3, 3, 5, 5, 4])

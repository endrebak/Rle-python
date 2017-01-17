from rle.rle import Rle
import pytest


class TestClass:

    def test_add_to_empty_rle(self):
        assert Rle().add(1, 3) == Rle([1], [3])

    def test_add_implicit_multiplicity(self):
        assert Rle([3, 4], [2, 3]).add(1) == Rle([3, 4, 1], [2, 3, 1])

    def test_add_different_then_last(self):
        assert Rle([3, 4]).add(5, 2) == Rle([3, 4, 5], [1, 1, 2])

    def test_add_same_as_last(self):
        assert Rle([3, 4]).add(4, 7) == Rle([3, 4], [1, 8])

    def test_0_multiplicity(self):
        with pytest.raises(AssertionError):
            Rle([1, 2, 3]).add(1, 0)

    def test_negative_multiplicity(self):
        with pytest.raises(AssertionError):
            Rle([1, 2, 3]).add(1, -5)

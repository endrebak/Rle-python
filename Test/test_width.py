from ..RleClass.Rle import *

# width should be the same as runLength


class TestClass:

    def test_empty_Rle(self):
        assert Rle().run_length() == Rle().width()

    def test_example(self):
        assert Rle([1, 1, 3, 4], [2, 3, 1, 2]).run_length() == Rle(
            [1, 1, 3, 4], [2, 3, 1, 2]).width()

from ...RleClass import Rle


class TestClass:

    def test_empty_constructor(self):
        assert Rle().length() == 0

    def test_multiplicity(self):
        assert Rle([1, 1, 4]) == Rle([1, 1, 4], [1, 1, 1])

    def test_compression(self):
        assert Rle([1, 1, 1, 3, 3, 1], [4, 1, 2, 6, 5, 1]
                   ) == Rle([1, 3, 1], [7, 11, 1])

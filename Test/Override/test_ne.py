from ...RleClass import Rle


class TestClass:

    def test_eq_empty_Rle(self):
        assert not (Rle() != Rle())

    def test_eq_example(self):
        assert not (Rle([1, 1, 1, 4]) != Rle([1, 4], [3, 1]))

    def test_not_eq_with_empty_Rle(self):
        assert Rle([1, 1]) != Rle()

    def test_not_eq_example(self):
        assert Rle([1, 1, 3, 4]) != Rle([1, 1, 4, 3])

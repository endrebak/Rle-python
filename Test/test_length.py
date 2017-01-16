from ..RleClass import Rle


class TestClass:

    def test_empty_Rle(self):
        assert Rle().length() == 0

    def test_example(self):
        assert Rle([1, 1, 3, 4], [2, 3, 1, 2]).length() == 8

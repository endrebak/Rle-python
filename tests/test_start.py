from rle.rle import Rle


class TestClass:

    def test_empty_Rle(self):
        assert Rle().start() == []

    def test_example(self):
        assert Rle([1, 1, 3, 4], [2, 3, 1, 2]).start() == [1, 6, 7]

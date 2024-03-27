import unittest
from src.normalization.test_normal_form import is_bcnf, is_3nf
from src.utils.binary_word import BinaryWord


class TestBCNFCheck(unittest.TestCase):
    def setUp(self):
        # Duplicate; will be moved later on a data file
        self.fd = [(BinaryWord(5, 3), BinaryWord(5, 28)), (BinaryWord(5, 5), BinaryWord(5, 26)),
                     (BinaryWord(5, 2), BinaryWord(5, 4)), (BinaryWord(5, 4), BinaryWord(5, 2)),
                     (BinaryWord(5, 4), BinaryWord(5, 8)), (BinaryWord(5, 2), BinaryWord(5, 16)),
                     (BinaryWord(5, 4), BinaryWord(5, 16))]


        # AB -> CDE, AC -> BDE, BC -> C
        self.fd_bcnf = [(BinaryWord(5, 3), BinaryWord(5, 28)), (BinaryWord(5, 5), BinaryWord(5, 26)),
                        (BinaryWord(5, 6), BinaryWord(5, 4))]

    def test_is_bcnf(self):
        # False
        self.assertFalse(
            is_bcnf(5, self.fd),
            "The relation is not in BCNF"
        )

        # True
        self.assertTrue(
            is_bcnf(5, self.fd_bcnf),
            "The relation is in BCNF"
        )


class Test3NFCheck(unittest.TestCase):
    def setUp(self):
        # A -> B, B -> C
        self.fd_2nf_not_3nf = [(BinaryWord(3, 1), BinaryWord(3, 2)), (BinaryWord(3, 2), BinaryWord(3, 4))]

        # AB -> CDE, AC -> BDE, BC -> C
        self.fd_bcnf = [(BinaryWord(5, 3), BinaryWord(5, 28)), (BinaryWord(5, 5), BinaryWord(5, 26)),
                        (BinaryWord(5, 6), BinaryWord(5, 4))]
    def test_is_3nf(self):
        self.assertFalse(
            is_3nf(self.fd_2nf_not_3nf)
        )

        self.assertTrue(
            is_3nf(self.fd_bcnf)
        )

if __name__ == '__main__':
    unittest.main()

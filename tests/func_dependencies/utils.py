import unittest
from src.func_dependencies.utils import attribute_closure, is_superkey, candidate_keys
from src.utils.binary_word import BinaryWord


class TestFunctionalDependencies(unittest.TestCase):

    def setUp(self):
        # R(A,B,C,D,E) with FDs: {{A,B} -> {C,D,E}, {A,C} -> {B,D,E}, B -> C, C -> B, C -> D, B -> E, C -> E}
        # Binary: 00011 -> 11100, 00101 -> 11010, 010 -> 100, 100 -> 010, 0100 -> 1000, 00010 -> 10000, 00100 -> 10000
        self.fd_2 = [(BinaryWord(5, 3), BinaryWord(5, 28)), (BinaryWord(5, 5), BinaryWord(5, 26)),
                      (BinaryWord(5, 2), BinaryWord(5, 4)), (BinaryWord(5, 4), BinaryWord(5, 2)),
                      (BinaryWord(5, 4), BinaryWord(5, 8)), (BinaryWord(5, 2), BinaryWord(5, 16)),
                      (BinaryWord(5, 4), BinaryWord(5, 16))]

    def test_is_superkey(self):
        # Test case 1
        fds = [(BinaryWord(4, 1), BinaryWord(4, 2)), (BinaryWord(4, 4), BinaryWord(4, 1))]
        self.assertTrue(is_superkey(BinaryWord(4, 12), fds))

        # Test case 2
        self.assertTrue(is_superkey(BinaryWord(5, 3), self.fd_2))
        self.assertFalse(is_superkey(BinaryWord(5, 9), self.fd_2))

    def test_attribute_closure(self):
        # Test case for fds_2
        self.assertEqual(
            attribute_closure(BinaryWord(5, 2), self.fd_2),
            BinaryWord(5, 30),
            "{B}+ = {C}+ = {B,C,D,E} = binary 11110"
        )
        self.assertEqual(
            attribute_closure(BinaryWord(5, 4), self.fd_2),
            BinaryWord(5, 30),
            "{B}+ = {C}+ = {B,C,D,E} = binary 11110"
        )
        self.assertEqual(
            attribute_closure(BinaryWord(5, 9), self.fd_2),
            BinaryWord(5, 9),
            "{A,D}+ = {A,D} = binary 10001"
        )

    def test_candidate_keys(self):
        self.assertEqual(
            candidate_keys(self.fd_2),
            {BinaryWord(5, 3), BinaryWord(5, 5)}
        )


if __name__ == '__main__':
    unittest.main()

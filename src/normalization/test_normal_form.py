from src.func_dependencies.utils import is_superkey
from src.utils.binary_word import BinaryWord


def is_bcnf(length: int, fds: list) -> bool:
    """
    Checks if a relation is in BCNF given a set of functional dependencies.

    Args:
        length (int): The number of attributes in the relation.
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        bool: True if the relation is in BCNF, False otherwise.
    """
    for left_side, right_side in fds:
        is_trivial = (left_side & right_side) == right_side
        if not is_trivial and not is_superkey(left_side, fds):
            return False
    return True

from functools import reduce

from src.func_dependencies.utils import candidate_keys, is_superkey
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


def is_3nf(fds: list[(BinaryWord, BinaryWord)]) -> bool:
    """
    Checks if a relation is in 3NF given a set of functional dependencies.

    Args:
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        bool: True if the relation is in 3NF, False otherwise.
    """
    prime_attributes = reduce(lambda acc, curr: acc | curr, candidate_keys(fds))

    for left_side, right_side in fds:
        is_trivial = (left_side & right_side) == right_side

        # If FD has a transitive dependency
        # (i.e. a dependency X -> Y where neither X nor Y contain prime attributes).
        if (not is_trivial and
                left_side & prime_attributes == prime_attributes.zeroes() and
                right_side & prime_attributes == prime_attributes.zeroes()):
            return False
    return True

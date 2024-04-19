from functools import reduce

from src.func_dependencies.utils import candidate_keys, is_superkey, is_subset_of, is_proper_subset_of
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
    cand_keys = candidate_keys(fds)
    prime_attributes = reduce(lambda acc, curr: acc | curr, cand_keys)

    for left_side, right_side in fds:
        is_trivial = is_subset_of(right_side, left_side)

        # If FD has a transitive dependency
        # (i.e. a dependency X -> Y where X is not a superkey and Y is not a prime attribute).
        if (not is_trivial and
                not is_subset_of(right_side, prime_attributes) and
                not reduce(lambda acc, curr: acc or is_subset_of(curr, left_side), cand_keys, False)):
            return False
    return True


def is_2nf(fds: list[(BinaryWord, BinaryWord)]) -> bool:
    """
    Checks if a relation is in 2NF given a set of functional dependencies.

    Args:
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        bool: True if the relation is in 2NF, False otherwise.
    """
    candidates = candidate_keys(fds)

    for left_side, right_side in fds:
        is_trivial = is_subset_of(right_side, left_side)

        # If FD has a partial dependency
        # (i.e. a candidate key C and a dependency X -> Y where X is a proper subset of C)
        if not is_trivial:
            for candidate in candidates:
                if is_proper_subset_of(left_side, candidate):
                    return False
    return True


class NormalFormChecker:
    """
    Combines the normalization tests into a single class.
    """
    def __init__(self, num_attr, fds: list[(BinaryWord, BinaryWord)]):
        self.fds = fds
        self.candidates = None
        self.num_attr = num_attr

    def is_bcnf(self) -> bool:
        return is_bcnf(self.num_attr, self.fds)

    def is_3nf(self) -> bool:
        self.candidates = candidate_keys(self.fds)
        prime_attributes = reduce(lambda acc, curr: acc | curr, self.candidates)

        for left_side, right_side in self.fds:
            is_trivial = is_subset_of(right_side, left_side)

            # If FD has a transitive dependency
            # (i.e. a dependency X -> Y where X is not a superkey and Y is not a prime attribute).
            if (not is_trivial and
                    not is_subset_of(right_side, prime_attributes) and
                    not reduce(lambda acc, curr: acc or is_subset_of(curr, left_side), self.candidates, False)):
                return False
        return True

    def is_2nf(self) -> bool:
        for left_side, right_side in self.fds:
            is_trivial = is_subset_of(right_side, left_side)

            # If FD has a partial dependency
            # (i.e. a candidate key C and a dependency X -> Y where X is a proper subset of C)
            if not is_trivial:
                for candidate in self.candidates:
                    if is_proper_subset_of(left_side, candidate):
                        return False
        return True
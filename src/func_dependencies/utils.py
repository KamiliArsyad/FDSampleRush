from itertools import combinations
from src.utils.binary_word import BinaryWord


def attribute_closure(attribute_set: BinaryWord, fds: list) -> BinaryWord:
    """
    Computes the closure of a set of attributes given a set of functional dependencies.

    Args:
        attribute_set (BinaryWord): A BinaryWord representing the set of attributes.
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        BinaryWord: The closure of the given set of attributes.
    """
    attr_closure = attribute_set
    has_changed = True

    while has_changed:
        has_changed = False

        for left_side, right_side in fds:
            # If the left side of the FD is a subset of the current closure
            # (i.e., all bits in left_side are set in attr_closure),
            # then add the attributes from the right side to the closure.
            if (left_side & attr_closure) == left_side:
                new_closure = attr_closure | right_side

                # If adding the right side of the FD to the closure introduces new attributes,
                # update the closure and set the flag to run another iteration.
                if new_closure != attr_closure:
                    attr_closure = new_closure
                    has_changed = True

    return attr_closure


def is_superkey(attribute_set: BinaryWord, fds: list[(BinaryWord, BinaryWord)]) -> bool:
    """
    Checks if a set of attributes is a superkey given a set of functional dependencies.

    Args:
        attribute_set (BinaryWord): A BinaryWord representing the set of attributes.
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        bool: True if the given set of attributes is a superkey, False otherwise.
    """
    return attribute_closure(attribute_set, fds) == BinaryWord(len(attribute_set), 2 ** len(attribute_set) - 1)


def candidate_keys(fds: list[(BinaryWord, BinaryWord)]) -> set[BinaryWord]:
    """
    Returns a set of candidate keys given a set of functional dependencies.

    Args:
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side).

    Returns:
        set[BinaryWord]: Set of candidate keys of the given set of functional dependencies.
    """
    candidates = set()
    non_trivial_fds = non_trivial(fds)
    if len(non_trivial_fds) == 0:
        return {fds[0][0].ones()}

    num_attrs = len(fds[0][0])

    for i in range(num_attrs):
        attr_set_comb = attribute_combinations(num_attrs, i, candidates)

        for attr_set in attr_set_comb:
            if is_superkey(attr_set, non_trivial_fds):
                candidates.add(attr_set)

    # Return the set difference of superkeys and non-minimal keys (i.e. minimal superkeys)
    return candidates


def non_trivial(fds: list[(BinaryWord, BinaryWord)]) -> list[(BinaryWord, BinaryWord)]:
    """
    Removes all trivial functional dependencies from the given list of functional dependencies.

    Args:
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side).

    Returns:
        list[(BinaryWord, BinaryWord)]: List of functional dependencies without trivial dependencies.
    """
    return filter(lambda fd: is_subset_of(fd[1], fd[2]), fds)


def attribute_combinations(n: int, c: int, exclude: set[BinaryWord] = None) -> set[BinaryWord]:
    """
    Returns a set of all possible attribute combinations given the number of attributes and number of chosen attributes.
    An exclude set is used to exclude all attributes which is a superset of any attributes in the given set.

    Args:
        n (int): Number of attributes.
        c: Number of chosen attributes.
        exclude (set[BinaryWord], optional): An optional set of attributes to exclude from the result.

    Returns:
        set[BinaryWord]: Set of all possible attribute combinations.
    """
    if exclude is None:
        exclude = set()

    result = set()
    for indices in combinations(range(n), c):
        attributes = BinaryWord(n)
        for index in indices:
            attributes = attributes.set_bit(index, 1)

        should_add = True
        for word in exclude:
            if is_subset_of(word, attributes):
                should_add = False
                break

        if should_add:
            result.add(attributes)

    return result


def is_subset_of(left_attributes: BinaryWord, right_attributes: BinaryWord) -> bool:
    """
    Checks whether the left set of attributes is a subset of the right set of attributes.

    Args:
        left_attributes: The left set of attributes.
        right_attributes: The right set of attributes.

    Returns:
        True if right_attributes are subset of left_attributes, False otherwise.
    """
    return (left_attributes & right_attributes) == left_attributes


def is_proper_subset_of(left_attributes: BinaryWord, right_attributes: BinaryWord) -> bool:
    """
    Checks whether the left set of attributes is a proper subset of the right set of attributes.

    Args:
        left_attributes: The left set attributes.
        right_attributes: The right set attributes.

    Returns:
        True if right_attributes are proper subset of left_attributes
    """
    return (left_attributes & right_attributes) == left_attributes and left_attributes < right_attributes

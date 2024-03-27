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
        fds: (list of tuples): A list where each tuple represents a functional dependency
                               as a pair of BinaryWords (left_side).

    Returns:
        set[BinaryWord]: Set of candidate keys of the given set of functional dependencies.
    """
    superkeys = set()
    for left_side, right_side in fds:
        closure = attribute_closure(left_side, fds)

        # If the left side of the FD is a superkey,
        # add the set of attributes to the list of superkeys.
        if closure == right_side.ones():
            superkeys.add(left_side)

    non_minimal_keys = set()
    for key in superkeys:
        for other_key in superkeys:

            # If key is a proper superset of another key,
            # add key to the set of non-minimal keys.
            if key != other_key and is_proper_subset_of(other_key, key):
                non_minimal_keys.add(key)
                break

    # Return the set difference of superkeys and non-minimal keys (i.e. minimal superkeys)
    return superkeys - non_minimal_keys


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

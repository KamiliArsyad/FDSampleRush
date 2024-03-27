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

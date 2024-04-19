from itertools import combinations
from src.utils.binary_word import BinaryWord


def attribute_closure(attribute_set: BinaryWord,
                      fds: list[(BinaryWord, BinaryWord)],
                      exclude: set[(BinaryWord, BinaryWord)] = None) -> BinaryWord:
    """
    Computes the closure of a set of attributes given a set of functional dependencies.

    Args:
        attribute_set (BinaryWord): A BinaryWord representing the set of attributes.
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).
        exclude (set of tuples, optional): An optional set of functional dependencies to exclude from the closure.

    Returns:
        BinaryWord: The closure of the given set of attributes.
    """
    attr_closure = attribute_set
    has_changed = True

    while has_changed:
        has_changed = False

        for i in range(len(fds)):
            if fds[i] is None:
                continue
            left_side, right_side = fds[i]
            if exclude is not None and (left_side, right_side) in exclude:
                continue
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
    return list(filter(lambda fd: not is_subset_of(fd[1], fd[0]), fds))


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

def drop_dependencies(fds: list[(BinaryWord, BinaryWord)]) -> list[(BinaryWord, BinaryWord)]:
    """
    Decompose RHS of every functional dependency to single attributes.

    Args:
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        list[(BinaryWord, BinaryWord)]: List of functional dependencies with single attributes on the RHS.
    """
    new_fds = []
    for left, right in fds:
        for i in range(len(right)):
            if right[i] == 1:
                new_fds.append((left, BinaryWord(len(right), 2 ** i)))
    return new_fds


def minimize_left(fds: list[(BinaryWord, BinaryWord)]) -> list[(BinaryWord, BinaryWord)]:
    """
    Minimize the left side of the functional dependencies.

    Args:
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        list[(BinaryWord, BinaryWord)]: List of functional dependencies with minimized left side.
    """
    new_fds = fds.copy()
    for word_index in range(len(new_fds)):
        left, right = new_fds[word_index]
        if left.pop_count() == 1:
            continue
        for i in range(len(left)):
            if left[i] == 0:
                continue

            exc_closure = attribute_closure(left.flip_bit(i), new_fds)

            if is_subset_of(right, exc_closure):
                left_new = left.set_bit(i, 0)
                left = left_new
                new_fds[word_index] = (left_new, right)

    unique_fds = set(FunctionalDependency(left, right) for left, right in new_fds)
    return [fd.get_value() for fd in unique_fds]


def minimize_left_explode(fds: list[(BinaryWord, BinaryWord)]) -> list[list[(BinaryWord, BinaryWord)]]:
    """
    Minimize the left side of the functional dependencies. Create a list of all possible minimized FDs.
    :param fds: List of functional dependencies
    :return: List of minimized FDs
    """
    new_fds = fds.copy()
    new_fds = non_trivial(new_fds)
    minimized_variants = [new_fds]
    # List of sets to build along the way
    minimized_variants_list_of_hashable_sets = [set()]

    # Invariant: minimized_variants[x][0...i] is minimized and unique for all x
    for i in range(len(new_fds)):
        left, right = new_fds[i]
        if left.pop_count() == 1:
            # Singular attribute LHS is already minimized by definition
            minimized_variants_list_of_hashable_sets[0].add(FunctionalDependency(left, right))
            continue

        # ------------------ Add optimization for two attributes later ------------------
        # ------------------ end ------------------

        num_to_process = len(minimized_variants)
        for variant_index in range(num_to_process):
            fd_list_variant = minimized_variants[variant_index]

            # Check all possible subsets of the left side
            attr_indices = [i for i in range(len(left)) if left[i] == 1]
            num_attrs = len(attr_indices)
            possible_minimal_fd_replacement = []

            for num_attribute_selected in range(1, num_attrs + 1):
                for subset in combinations(attr_indices, num_attribute_selected):
                    new_left = BinaryWord(len(left), sum(2 ** index for index in subset))

                    skip = False
                    for minimum_replacement in possible_minimal_fd_replacement:
                        if is_subset_of(minimum_replacement, new_left):
                            # The new_left is not minimal; skip to the next subset
                            skip = True
                            break
                    if skip:
                        continue

                    exc_closure = attribute_closure(new_left, fd_list_variant)
                    if is_subset_of(right, exc_closure):
                        possible_minimal_fd_replacement.append(new_left)

            is_first = True
            for new_left in possible_minimal_fd_replacement:
                if is_first:
                    fd_list_variant[i] = (new_left, right)
                    is_first = False

                    minimized_variants_list_of_hashable_sets[variant_index].add(FunctionalDependency(new_left, right))
                else:
                    new_fd = FunctionalDependency(new_left, right)
                    # Avoid duplicates and create new progress set for the soon-to-be appended new list
                    if new_fd in minimized_variants_list_of_hashable_sets[variant_index]:
                        continue
                    progress_set_copy = minimized_variants_list_of_hashable_sets[variant_index].copy()
                    progress_set_copy.add(new_fd)
                    minimized_variants_list_of_hashable_sets.append(progress_set_copy)
                    # --------------------------------------------

                    # Main Operation: Append a new list with the new FD
                    latest_copy = fd_list_variant.copy()
                    latest_copy[i] = new_fd.get_value()
                    minimized_variants.append(latest_copy)

    return minimized_variants


def minimize_right(fds: list[(BinaryWord, BinaryWord)]) -> list[(BinaryWord, BinaryWord)]:
    """
    Minimize the right side of the functional dependencies.

    Args:
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        list[(BinaryWord, BinaryWord)]: List of functional dependencies with minimized right side.
    """
    new_fds = fds.copy()
    new_fds = non_trivial(new_fds)
    for i in range(len(new_fds)):
        left, right = new_fds[i]
        closure_exclude = attribute_closure(left, new_fds, {(left, right)})
        if is_subset_of(right, closure_exclude):
            new_fds[i] = None

    return list(filter(lambda x: x is not None, new_fds))

def minimize_right_explode(fds: list[(BinaryWord, BinaryWord)]) -> list[list[(BinaryWord, BinaryWord)]]:
    """
    Generates all possible minimized FDs by minimizing the right side of the FDs.
    :param fds: List of functional dependencies
    :return: List of sets of RHS-minimized FDs
    """
    # Remove trivial FDs
    new_fds = non_trivial(fds)
    minimized_variants = [new_fds.copy()]

    for fd_index in range(len(new_fds)):
        left, right = new_fds[fd_index]
        prev_minimized_variants = minimized_variants.copy()
        minimized_variants = []

        for variant in prev_minimized_variants:
            closure_exclude = attribute_closure(left, variant, {(left, right)})
            if is_subset_of(right, closure_exclude):
                new_variant = variant.copy()
                new_variant[fd_index] = None
                minimized_variants.append(new_variant)
            minimized_variants.append(variant.copy())

        # minimized_variants.extend([variant for variant in prev_minimized_variants if variant not in minimized_variants])

    for variant_index in range(len(minimized_variants)):
        variant = minimized_variants[variant_index]
        variant = list(filter(lambda x: x is not None, variant))

        # Sort by the string representation of the FDs
        variant.sort(key=lambda x: str(x))
        set_variant = set(FunctionalDependency(left, right) for left, right in variant)
        minimized_variants[variant_index] = [fd.get_value() for fd in set_variant]

    minimized_variants = sorted(minimized_variants, key=lambda x: len(x))

    # Remove non-minimal subsets: S1 = [F1, F2, F3], S2 = [F1, F2] -> S1 is non-minimal as S2 is a subset
    index_x = 0
    while index_x < len(minimized_variants):
        variant_x = minimized_variants[index_x]
        index_x += 1
        for index_y in range(len(minimized_variants)):
            variant_y = minimized_variants[index_y]
            if len(variant_x) < len(variant_y) or index_x - 1 == index_y:
                continue

            if len(variant_x) == len(variant_y):
                same = True
                for fd in variant_x:
                    if fd not in variant_y:
                        same = False
                        break

                if same:
                    minimized_variants.remove(variant_x)
                    index_x -= 1
                    break

            remove = True

            for fd in variant_y:
                if fd not in variant_x:
                    remove = False
                    break

            go_next = False
            if remove:
                minimized_variants.remove(variant_x)
                index_x -= 1
                break

    return minimized_variants


def compact(fds: list[(BinaryWord, BinaryWord)]) -> list[(BinaryWord, BinaryWord)]:
    """
    Compact the given list of functional dependencies.

    Args:
        fds (list of tuples): A list where each tuple represents a functional dependency
                              as a pair of BinaryWords (left_side, right_side).

    Returns:
        list[(BinaryWord, BinaryWord)]: List of compacted functional dependencies.
    """
    new_fds = {}
    for left, right in fds:
        if left in new_fds:
            new_fds[left] = new_fds[left] | right
        else:
            new_fds[left] = right
    return [(left, right) for left, right in new_fds.items()]


def sigma_plus_limited(fds: list[(BinaryWord, BinaryWord)]) -> list[(BinaryWord, BinaryWord)]:
    candidates = set()
    sigma_plus = set()
    non_trivial_fds = non_trivial(fds)
    if len(non_trivial_fds) == 0:
        return fds[0][0].ones()

    num_attrs = len(fds[0][0])

    for i in range(num_attrs):
        attr_set_comb = attribute_combinations(num_attrs, i, candidates)

        for attr_set in attr_set_comb:
            attr_closure = attribute_closure(attr_set, non_trivial_fds)
            if attr_closure.pop_count == fds[0][0].length:
                candidates.add(attr_set)

            sigma_plus.add(FunctionalDependency(attr_set, attr_closure))

    fd_values = [fd.get_value() for fd in sigma_plus]



    return fd_values

class FunctionalDependency:
    def __init__(self, lhs: tuple[BinaryWord], rhs: tuple[BinaryWord]):
        self.lhs = lhs  # Left-hand side of the FD
        self.rhs = rhs  # Right-hand side of the FD

    def __repr__(self):
        return f"FD(lhs={self.lhs}, rhs={self.rhs})"

    def __eq__(self, other):
        if not isinstance(other, FunctionalDependency):
            return NotImplemented
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def get_value(self):
        # Example method to easily retrieve the BinaryWords in this FD
        return (self.lhs, self.rhs)


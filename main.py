from src.utils.misc import FDBinaryAdapter
from src.func_dependencies.utils import *
from src.utils.binary_word import BinaryWord


def min_cover(fds):
    adapter = FDBinaryAdapter(FDBinaryAdapter.create_attribute_list(fds))
    binary_fds = adapter.translate_to_binary(fds)
    dropped = drop_dependencies(binary_fds)
    dropped = non_trivial(dropped)
    minimized_left = minimize_left(dropped)
    minimized_right = minimize_right(minimized_left)

    return adapter.translate_from_binary(minimized_right)


def min_covers(fds):
    adapter = FDBinaryAdapter(FDBinaryAdapter.create_attribute_list(fds))
    binary_fds = adapter.translate_to_binary(fds)

    min_covers_list = min_covers_binary(binary_fds)

    return [adapter.translate_from_binary(fd) for fd in min_covers_list]

def min_covers_binary(fds):
    dropped = drop_dependencies(fds)
    dropped = non_trivial(dropped)
    minimized_left = minimize_left_explode(dropped)
    min_covers_list = []
    for candidate_cover in minimized_left:
        min_covers_list.extend(minimize_right_explode(candidate_cover))

    # Remove duplicates
    for i in range(len(min_covers_list)):
        for j in range(i + 1, len(min_covers_list)):
            if min_covers_list[i] == min_covers_list[j]:
                min_covers_list[j] = None

    min_covers_list = [cover for cover in min_covers_list if cover is not None]

    return min_covers_list


def all_minimal_covers_binary(fds):
    dropped = drop_dependencies(fds)
    dropped = non_trivial(dropped)

    sigma_plus = sigma_plus_limited(dropped)

    return min_covers_binary(sigma_plus)


def all_minimal_covers(fds):
    adapter = FDBinaryAdapter(FDBinaryAdapter.create_attribute_list(fds))
    binary_fds = adapter.translate_to_binary(fds)

    min_covers_list = all_minimal_covers_binary(binary_fds)

    return [adapter.translate_from_binary(fd) for fd in min_covers_list]


def sigma_plus_limited_string(fds):
    adapter = FDBinaryAdapter(FDBinaryAdapter.create_attribute_list(fds))
    binary_fds = adapter.translate_to_binary(fds)

    candidate_keys_list = sigma_plus_limited(binary_fds)

    return adapter.translate_from_binary(candidate_keys_list)

if __name__ == '__main__':
    fd_2 = [(BinaryWord(5, 3), BinaryWord(5, 28)), (BinaryWord(5, 5), BinaryWord(5, 26)),
             (BinaryWord(5, 4), BinaryWord(5, 16))]
    fd_3 = [(BinaryWord(6, 32), BinaryWord(6, 24)),
            (BinaryWord(6, 16), BinaryWord(6, 12)),
            (BinaryWord(6, 4), BinaryWord(6, 16)),
            (BinaryWord(6, 50), BinaryWord(6, 1))]
    # fds = [[['A'], ['A', 'B']], [['B'], ['A', 'C']], [['A'], ['C']], [['A', 'B'], ['C']]]
    # fds = [[['A'], ['A', 'B']], [['B'], ['A', 'C']], [['A'], ['C']], [['A', 'B', 'D'], ['C']], [['D'], ['C']]]
    # A -> B, B -> C, AD -> C, AE -> C, D -> B, E -> B
    # fds = [[['A'], ['B']], [['B'], ['C']], [['A', 'D'], ['C']], [['A', 'E'], ['C']], [['D'], ['B']], [['E'], ['B']]]
    # fds = [[['A'], ['B']], [['B'], ['C']], [['A', 'D'], ['C']], [['A', 'E'], ['C']]]
    # ABC -> D, B -> C, C -> B
    fds = [[['A', 'B', 'C'], ['D']], [['B'], ['C']], [['C'], ['B']]]
    # fds = [[[], ['B']], [['B'], ['C']], [['C'], ['A']]]
    # min_cov = min_covers(fds)
    min_cov = sigma_plus_limited_string(fds)
    # sort by lhs values
    min_cov = sorted(min_cov, key=lambda x: x[0])
    # sort by length of lhs
    min_cov = sorted(min_cov, key=lambda x: len(x[0]))
    # print line by line
    for fd in min_cov:
        print(fd)


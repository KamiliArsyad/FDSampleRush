import time
from typing import Tuple

from numpy import random, zeros

from src.func_dependencies.generator import FDGenerator
from src.normalization import test_normal_form
from src.utils.binary_word import BinaryWord


class FDSampleRushResult:
    """
    Stores the result of a sample rush.

    Attributes:
        num_attributes (int): The number of attributes in the relation.
        fds (list[(BinaryWord, BinaryWord)]): The functional dependencies of the relation.
        result_bcnf (bool): True if the relation is in BCNF, False otherwise.
        result_3nf (bool): True if the relation is in 3NF, False otherwise.
        result_2nf (bool): True if the relation is in 2NF, False otherwise.
        result_time (float): The time taken to process the relation.
    """
    def __init__(self, num_attributes: int, fds: list[Tuple[BinaryWord, BinaryWord]]):
        self.num_attributes = num_attributes
        self.fds = fds
        self.result_bcnf = False
        self.result_3nf = False
        self.result_2nf = False
        self.result_time = 0

    def run(self):
        """
        Starts the normalization tests.
        """
        start_time = time.time()
        normal_form_tester = test_normal_form.NormalFormChecker(self.num_attributes, self.fds)
        self.result_bcnf = normal_form_tester.is_bcnf()
        self.result_3nf = True if self.result_bcnf else normal_form_tester.is_3nf()
        self.result_2nf = True if self.result_3nf else normal_form_tester.is_2nf()
        self.result_time = time.time() - start_time

    @staticmethod
    def summarize(results: list['FDSampleRushResult']):
        """
        Summarizes the results of multiple sample rushes.

        Args:
            results (list[FDSampleRushResult]): List of results to summarize.

        Returns:
            dict: A dictionary containing the summary.
        """
        num_bcnf = sum(1 for result in results if result.result_bcnf)
        num_3nf = sum(1 for result in results if result.result_3nf)
        num_2nf = sum(1 for result in results if result.result_2nf)
        total_time = sum(result.result_time for result in results)

        return {
            'num_bcnf': num_bcnf,
            'num_3nf': num_3nf,
            'num_2nf': num_2nf,
            'total_time': total_time
        }

    def __str__(self):
        return f'Num_attributes: {self.num_attributes}\n' \
               f'BCNF: {self.result_bcnf}\n' \
               f'3NF: {self.result_3nf}\n' \
               f'2NF: {self.result_2nf}\n' \
               f'Number of FDs: {len(self.fds)}\n' \
               f'Time: {self.result_time}'

    def __repr__(self):
        return self.__str__()


def rand_binomial_binary(bit_len: int, p: float) -> int:
    """
    Generate a binary word of the given length where each bit is set to 1 with a binomial distribution.
    :param bit_len: The length of the binary word in bits.
    :param p: The probability of setting a bit to 1.
    :return: A binary word of the given length.
    """
    res = BinaryWord(bit_len)
    for i in range(bit_len):
        if random.random() < p:
            res = res.set_bit(i, 1)
    return res.value


class FDSampleRush:
    """
    Runner for the FD sampler.
    """
    def __init__(self, num_attributes: int):
        self.num_attributes = num_attributes
        self.num_fd_kwargs = {0, self.num_attributes}
        self.num_fd_distribution = random.randint

        self.generator = FDGenerator(num_attributes)
        self.results = []

    def set_fd_distribution(self, distribution: callable, **kwargs):
        """
        Sets the distribution for generating functional dependencies.
        It is expected that the distribution function generates a binary word of the given length or is a rv_continuous.
        :param distribution: The distribution to use for generating functional dependencies.
        :param kwargs: Additional arguments to pass to the distribution function.
        """
        self.generator = FDGenerator(self.num_attributes, distribution, **kwargs)

    def set_num_fd_distribution(self, distribution: callable, **kwargs):
        """
        Sets the distribution for generating the number of functional dependencies.
        :param distribution: The distribution to use for generating the number of functional dependencies.
        :param kwargs: Additional arguments to pass to the distribution function.
        """
        self.num_fd_distribution = distribution
        self.num_fd_kwargs = kwargs

    def run(self, timeout_seconds: int, debug: bool):
        start_time = time.time()
        sample_num = 0

        while True:
            if time.time() - start_time > timeout_seconds:
                break
            sample_num += 1

            m = self.num_fd_distribution(*self.num_fd_kwargs)
            fds = self.generator.generate_m_fds(m)

            FDSampleRush.print_debug(debug, 'Test case:', sample_num, 'Number of FDs:', m)
            FDSampleRush.print_debug(debug, fds)
            result = FDSampleRushResult(self.num_attributes, fds)
            result.run()
            self.results.append(result)
            FDSampleRush.print_debug(debug, result)
            FDSampleRush.print_debug(debug, 'Finished test case:' + str(sample_num) + '\n' + '-'*50)

    def get_results(self) -> list[FDSampleRushResult]:
        return self.results

    @staticmethod
    def print_debug(is_debug: bool, *args):
        if not is_debug:
            return
        print(*args)


class FDBinaryAdapter:
    def __init__(self, attributes):
        # Assuming attributes is a list of unique attribute names
        self.attribute_indices = {attr: index for index, attr in enumerate(attributes)}
        self.attributes = attributes  # To translate back from binary to strings

    def translate_to_binary(self, fds):
        return [(self._fd_to_binary(fd[0]), self._fd_to_binary(fd[1])) for fd in fds]

    def translate_from_binary(self, binary_fds):
        return [[self._binary_to_fd(bw) for bw in fd] for fd in binary_fds]

    def _fd_to_binary(self, attr_list):
        # Initialize a binary representation with all zeros
        binary_rep = zeros(len(self.attribute_indices), dtype=int)
        for attr in attr_list:
            # Set the bit at the index corresponding to the attribute
            index = self.attribute_indices[attr]
            binary_rep[index] = 1
        # Convert the binary array to a binary word
        return BinaryWord(len(self.attribute_indices), int(''.join(map(str, binary_rep)), 2))

    def _binary_to_fd(self, binary_word):
        # Convert the binary word to its binary string representation
        binary_str = format(binary_word.value, f'0{binary_word.length}b')
        # Find which bits are set and translate back to the attribute names
        return [self.attributes[idx] for idx, bit in enumerate(binary_str) if bit == '1']

    @staticmethod
    def create_attribute_list(fds_list):
        """
        Creates a list of unique attributes from a set of functional dependencies.

        :param fds_list: A list of functional dependencies, where each dependency is
                         represented as a list of two lists.
        :return: A list of unique attributes.
        """
        attributes = set()
        for fd in fds_list:
            determinant, dependent = fd
            attributes.update(determinant)
            attributes.update(dependent)

        return sorted(list(attributes))



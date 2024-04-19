from math import comb

import numpy as np
import random
from src.utils.binary_word import BinaryWord

rv_continuous = 'HELLO'

class BinaryWordGenerator:
    """
    A class to generate binary words of a given length.

    Methods:
        random(length): Returns a random binary word of the given length.
        from_distribution(length, distribution, **kwargs): Returns a binary word generated from a given distribution.
        predictable_random(length, seed): Returns a predictable random binary word of the given length.
    """
    @staticmethod
    def random(length) -> BinaryWord:
        """
        Returns a random binary word of the given length.
        :param length: The length of the binary word in bits.
        :return: A random binary word of the given length.
        """
        value = np.random.randint(0, 2**length)
        return BinaryWord(length, value)

    @staticmethod
    def convert_number_of_ones_to_int(num_attributes_x, num_attributes_relation):
        binary_array = [1] * num_attributes_x + [0] * (num_attributes_relation - num_attributes_x)
        random.shuffle(binary_array)
        binary_string = ''.join(map(str, binary_array))
        value = int(binary_string, 2)
        return value

    @staticmethod
    def from_distribution(length, distribution='uniform', **kwargs) -> BinaryWord:
        """
        Returns a binary word generated from a given distribution.
        :param length: The length of the binary word in bits.
        :param distribution: The distribution to use for generating the binary word.
        :param kwargs: Additional arguments to pass to the distribution's rvs method.
        :return: A binary word generated from the given distribution.
        """
        if distribution == 'uniform':
            value = np.random.randint(0, 2**length)
        elif distribution == 'realistic':
            # based on distribution of size of X in X -> Y
            num_attributes_relation = 2**length
            num_attributes_x = random.choices(range(num_attributes_relation + 1),
                                   weights=np.array([comb(num_attributes_relation, i)
                                                     for i in range(num_attributes_relation + 1)])
                                           / sum([comb(20, i) for i in range(num_attributes_relation + 1)]),
                                   k=1)[0]
            value = BinaryWordGenerator.convert_number_of_ones_to_int(num_attributes_x, num_attributes_relation)

        elif isinstance(distribution, rv_continuous):
            # Using SciPy distribution to generate a number
            value = int(distribution.rvs(**kwargs) * (2**length))
        elif callable(distribution):
            value = int(distribution(**kwargs))
        else:
            raise ValueError("Unsupported distribution type")
        return BinaryWord(length, value)

    @staticmethod
    def predictable_random(length, seed) -> BinaryWord:
        """
        Returns a predictable random binary word of the given length.
        :param length: The length of the binary word in bits.
        :param seed: The seed to use for the random number generator.
        :return: A predictable random binary word of the given length.
        """
        np.random.seed(seed)
        value = np.random.randint(0, 2**length)
        return BinaryWord(length, value)


class FDGenerator:
    """
    A class to generate functional dependencies (FDs) represented as tuples of binary words.

    This class allows for the generation of functional dependencies between binary words,
    supporting both uniform random generation and generation based on a specified distribution.

    Attributes:
        k (int): The length of the binary words in the functional dependency.
        distribution (callable, optional): A function that generates random numbers used to
                                           determine the values of the binary words. If None,
                                           a uniform distribution is used.
        kwargs (dict): Additional keyword arguments to be passed to the distribution function.

    Methods:
        generate_fd(): Generates a functional dependency as a tuple of two binary words.
    """
    def __init__(self, k, distribution=None, **kwargs):
        self.k = k
        self.distribution = distribution
        self.kwargs = kwargs

    def generate_fd(self) -> (BinaryWord, BinaryWord):
        """
        Generates a functional dependency represented as a tuple (w1, w2),
        where w1 and w2 are binary words of length k.

        The method supports generating binary words based on a uniform distribution or
        a user-specified distribution provided during class initialization.

        Returns:
            tuple(BinaryWord, BinaryWord): A tuple representing the functional dependency,
                                           where each BinaryWord is of length k.
        """
        if self.distribution:
            w1_value = BinaryWordGenerator.from_distribution(self.k, self.distribution, **self.kwargs).value
            w2_value = BinaryWordGenerator.from_distribution(self.k, self.distribution, **self.kwargs).value
        else:
            w1 = BinaryWordGenerator.random(self.k)
            w2 = BinaryWordGenerator.random(self.k)
            return (w1, w2)

        w1 = BinaryWord(self.k, int(w1_value))
        w2 = BinaryWord(self.k, int(w2_value))
        return (w1, w2)

    def generate_m_fds(self, m: int) -> list[(BinaryWord, BinaryWord)]:
        """
        Generates a list of m unique functional dependencies.
        :param m: The number of functional dependencies to generate.
        :return: A list of m functional dependencies.
        """
        fds_set = set()
        while len(fds_set) < m:
            fds_set.add(self.generate_fd())
        return list(fds_set)

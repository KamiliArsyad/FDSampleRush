import numpy as np
from scipy.stats import rv_continuous

from src.utils.binary_word import BinaryWord


class BinaryWordGenerator:
    """
    A class to generate binary words of a given length.

    Methods:
        random(length): Returns a random binary word of the given length.
        from_distribution(length, distribution, **kwargs): Returns a binary word generated from a given distribution.
        predictable_random(length, seed): Returns a predictable random binary word of the given length.
    """
    @staticmethod
    def random(length):
        """
        Returns a random binary word of the given length.
        :param length: The length of the binary word in bits.
        :return: A random binary word of the given length.
        """
        value = np.random.randint(0, 2**length)
        return BinaryWord(length, value)

    @staticmethod
    def from_distribution(length, distribution='uniform', **kwargs):
        """
        Returns a binary word generated from a given distribution.
        :param length: The length of the binary word in bits.
        :param distribution: The distribution to use for generating the binary word.
        :param kwargs: Additional arguments to pass to the distribution's rvs method.
        :return: A binary word generated from the given distribution.
        """
        if distribution == 'uniform':
            value = np.random.randint(0, 2**length)
        elif isinstance(distribution, rv_continuous):
            # Using SciPy distribution to generate a number
            value = int(distribution.rvs(**kwargs) * (2**length))
        else:
            raise ValueError("Unsupported distribution type")
        return BinaryWord(length, value)

    @staticmethod
    def predictable_random(length, seed):
        """
        Returns a predictable random binary word of the given length.
        :param length: The length of the binary word in bits.
        :param seed: The seed to use for the random number generator.
        :return: A predictable random binary word of the given length.
        """
        np.random.seed(seed)
        value = np.random.randint(0, 2**length)
        return BinaryWord(length, value)

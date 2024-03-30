import time
from typing import Tuple

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
        self.result_bcnf = test_normal_form.is_bcnf(self.num_attributes, self.fds)
        self.result_3nf = True if self.result_bcnf else test_normal_form.is_3nf(self.fds)
        self.result_2nf = True if self.result_3nf else test_normal_form.is_2nf(self.fds)
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
               f'Time: {self.result_time}'

    def __repr__(self):
        return self.__str__()
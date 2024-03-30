import time

from src.func_dependencies.generator import FDGenerator
from src.normalization import test_normal_form
from src.utils.misc import FDSampleRushResult
from numpy import random


class FDSampleRush:
    def __init__(self, num_attributes: int):
        self.num_attributes = num_attributes
        self.generator = FDGenerator(num_attributes)
        self.results = []

    def run(self, timeout_seconds: int, debug: bool):
        start_time = time.time()
        sample_num = 0

        while True:
            if time.time() - start_time > timeout_seconds:
                break
            sample_num += 1

            m = random.randint(0, self.num_attributes)
            created_fds = set()
            fds = []
            count = 0
            while count < m:
                fd = self.generator.generate_fd()
                if fd in created_fds:
                    continue

                created_fds.add(fd)
                fds.append(fd)
                count += 1

            FDSampleRush.print_debug(debug, 'Test case:', sample_num, 'Number of FDs:', m)
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


if __name__ == '__main__':
    num_attributes = 17
    timeout_seconds = 600

    rush = FDSampleRush(num_attributes)
    rush.run(timeout_seconds, debug=True)
    print(FDSampleRushResult.summarize(rush.get_results()))
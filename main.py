from src.utils.misc import FDSampleRushResult, rand_binomial_binary, FDSampleRush

if __name__ == '__main__':
    num_attr = 5
    timeout = 12

    rush = FDSampleRush(num_attr)
    rush.set_fd_distribution(rand_binomial_binary, **{'bit_len': num_attr, 'p': 0.5})
    rush.run(timeout, debug=True)
    print(FDSampleRushResult.summarize(rush.get_results()))
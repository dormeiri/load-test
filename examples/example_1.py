import argparse
import logging
import sys

from examples.test_google import TestGoogle
from load_test.runner import Runner, ARG_LOGGER, ARG_PROCESSES, ARG_DURATION, ARG_RUNS, ARG_DELAY, ARG_RESULTS_DIR

TEST_CLASSES = [TestGoogle]


def main():
    options = parse_args()
    options[ARG_LOGGER] = init_logger()
    runner = Runner(TEST_CLASSES, options)
    runner.run()


def init_logger():
    log_format = logging.Formatter(f"%(asctime)s - %(levelname)s - %(message)s")
    handler_debug = logging.StreamHandler(sys.stdout)
    handler_debug.setLevel(logging.DEBUG)
    handler_debug.setFormatter(log_format)
    handler_debug.addFilter(lambda record: record.levelno < logging.WARNING)
    handler_warning = logging.StreamHandler(sys.stderr)
    handler_warning.setLevel(logging.WARNING)
    handler_warning.setFormatter(log_format)
    handler_warning.addFilter(lambda record: record.levelno >= logging.WARNING)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler_debug)
    logger.addHandler(handler_warning)
    return logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(f"--{ARG_PROCESSES}", help="amount of test duplicates running in parallel", type=int, default=1)
    parser.add_argument(f"--{ARG_DURATION}", help="test duration limit in seconds", type=int, default=3)
    parser.add_argument(f"--{ARG_RUNS}", help="test runs limit", type=int, default=None)
    parser.add_argument(f"--{ARG_DELAY}", help="delay between each batch run", type=int, default=3)
    parser.add_argument(ARG_RESULTS_DIR, help="directory of the results", type=str)
    return vars(parser.parse_args())


if __name__ == "__main__":
    main()

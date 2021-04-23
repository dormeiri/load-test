import logging
import os
import shutil
import time
from multiprocessing import Process

from load_test.test_base import TestBase

ARG_PROCESSES = "processes"
ARG_DURATION = "duration"
ARG_RUNS = "runs"
ARG_DELAY = "delay"
ARG_RESULTS_DIR = "results_dir"
ARG_LOGGER = "logger"

DEFAULT_PROCESSES = 1
DEFAULT_DURATION = 3
DEFAULT_RESULTS_DIR = "results"


class Runner:
    def __init__(self, tests_classes, options=None):
        options = options or {}
        self._tests_classes = tests_classes
        self._processes = options.get(ARG_PROCESSES, DEFAULT_PROCESSES)
        self._duration = options.get(ARG_DURATION, DEFAULT_DURATION)
        self._runs = options.get(ARG_RUNS)
        self._delay = options.get(ARG_DELAY)
        self._temp_results_dir = f"{options.get(ARG_RESULTS_DIR, DEFAULT_RESULTS_DIR)}/{int(time.time())}"
        self._logger = options.get(ARG_LOGGER) or logging.getLogger("dummy")
        self._validate()

    def run(self):
        tests_batches = self._get_tests_batches()
        self._logger.info(f"Running {len(tests_batches)} tests batches...")
        for batch_index, tests_batch in enumerate(tests_batches):
            self._logger.info(f"Running tests batch {batch_index}...")
            self._run_tests_batch(tests_batch)
            self._logger.info(f"Finished test batch {batch_index}")
            if self._delay and batch_index < len(tests_batches) - 1:
                time.sleep(self._delay)
        self._logger.info("Finished running tests batches")
        self._logger.info("Creating final result file...")
        self._combine_csv_files()
        self._logger.info("Finished creating final result file")

    def _get_tests_batches(self):
        return [self._get_tests_batch(i, test_cls) for i, test_cls in enumerate(self._tests_classes)]

    def _get_tests_batch(self, test_batch_index, test_cls):
        tests = []
        for i in range(self._processes):
            results_filename = f"{self._temp_results_dir}/{test_cls.get_test_case_name()}_{test_batch_index}_{i}.csv"
            test = test_cls(self._duration, self._runs, results_filename)
            tests.append(test)
        return tests

    def _combine_csv_files(self):
        with open(f"{self._temp_results_dir}.csv", 'w') as output_file:
            paths = (f"{self._temp_results_dir}/{filename}" for filename in os.listdir(self._temp_results_dir))

            first_path = next(paths)
            with open(first_path) as f:
                output_file.writelines(f)

            for path in paths:
                with open(path) as f:
                    next(f)
                    output_file.writelines(f)

        shutil.rmtree(self._temp_results_dir)

    def _validate(self):
        validations = (
            (all(issubclass(test_cls, TestBase) for test_cls in self._tests_classes), "Invalid tests class"),
            (self._processes > 0, "Number of processes must be a positive integer"),
            (self._duration > 0, "Duration must be a positive integer"),
            (self._runs is None or self._runs > 0, "Runs limit must be a positive integer")
        )

        invalid_message = "; ".join(message for is_valid, message in validations if not is_valid)
        if invalid_message:
            raise ValueError(invalid_message)

    @staticmethod
    def _run_tests_batch(tests_batch):
        processes = [Process(target=test.run_test_case) for test in tests_batch]

        for process in processes:
            process.start()

        for process in processes:
            process.join()

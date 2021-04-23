import csv
import math
import os
import time


class TestBase:
    def __init__(self, duration, runs, results_filename):
        self._results_filename = results_filename
        self._limit_time = duration
        self._limit_task_runs = runs
        self._run_start_time = None
        self._run_time = None
        self._successes = None
        self._failures = None
        self._task_start_time = None
        self._tasks_run_time = None
        self._last_error = None

    @classmethod
    def get_test_case_name(cls):
        return cls.__name__

    def _run_task(self):
        raise NotImplementedError()

    def run_test_case(self):
        self._pre_run()
        while not self._is_time_exceeded and not self._is_works_exceeded:
            self._pre_task()
            try:
                self._run_task()
                self._post_task()
            except Exception as err:
                self._post_task(err)
        self._post_run()

    def _pre_run(self):
        self._run_start_time = time.time()
        self._successes = 0
        self._failures = 0
        self._tasks_run_time = []

    def _pre_task(self):
        self._task_start_time = time.time()

    def _post_task(self, error=None):
        task_end_time = time.time()
        task_run_time = task_end_time - self._task_start_time
        self._tasks_run_time.append(task_run_time)
        self._run_time = task_end_time - self._run_start_time
        if error:
            self._last_error = error
            self._failures += 1
        else:
            self._successes += 1

    def _post_run(self):
        t_len = len(self._tasks_run_time)
        t_sum = sum(self._tasks_run_time)
        t_sum_sqr = sum(x ** 2 for x in self._tasks_run_time)
        t_mean = (t_sum / t_len) if t_len > 0 else math.nan
        t_std = (((t_sum_sqr / t_len) - (t_mean ** 2)) ** .5) if t_len > 1 else math.nan

        statistics = {
            "test_name": self.get_test_case_name(),
            "run_start_time": self._run_start_time,
            "successes": self._successes,
            "failures": self._failures,
            "task_run_time_count": t_len,
            "task_run_time_sum": t_sum,
            "task_run_time_sum_sqr": t_sum_sqr,
            "task_run_time_min": min(self._tasks_run_time),
            "task_run_time_max": max(self._tasks_run_time),
            "task_run_time_mean": t_mean,
            "task_run_time_std": t_std,
            "last_error": self._last_error
        }

        self._write_result(statistics)

    def _write_result(self, result):
        filename = self._results_filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(result.keys())
            csv_writer.writerow(result.values())

    @property
    def _is_time_exceeded(self):
        return self._run_time and self._run_time >= self._limit_time

    @property
    def _is_works_exceeded(self):
        return self._limit_task_runs and len(self._tasks_run_time) >= self._limit_task_runs

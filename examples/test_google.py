import requests as requests

from load_test.test_base import TestBase


class TestGoogle(TestBase):
    def _run_task(self):
        requests.get("https://google.com")

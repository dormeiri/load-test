import requests as requests

import load_test


class TestGoogle(load_test.TestBase):
    def _run_task(self):
        requests.get("https://google.com")

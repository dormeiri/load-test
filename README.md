# load-test

## Quick Start

Define by implementing `TestBase`, run with `Runner`

```python
import load_test

class MyTest(load_test.TestBase):
    def _run_task(self):
        requests.get("https://google.com")

def main():
    load_test.Runner([MyTest]).run()
```

_See [examples](/examples)_

## Get It Now

Run `pip install load_test`

## How It Works

Preconfigured amount of processes will run a test case over and over again until timeout. You can send more than one
test case and then after each test finishes, it will continue to the next one (after some delay).

Each process gathers statistics, when all tests finish the main process will create a single result file.

## Runner Options

|Option|Description|Default|
|:---:|---|:---:|
|`processes`|How many processes will run the test case in parallel|`1`|
|`duration`|How many seconds each process will run the test case over and over again|`3`|
|`results_dir`|The directory of the final results, the filename is the timestamp of the run|`"results"`|
|`runs`|The limit amount for each process to run the test definition (`None` for no limit)|`None`|
|`delay`|The delay in seconds between each test case (`None` for no delay)|`None`|
|`logger`|Logger for general log messages (`None` for no logger)|`None`|

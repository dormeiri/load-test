import load_test
from examples.test_google import TestGoogle


def main():
    runner = load_test.Runner([TestGoogle])
    runner.run()


if __name__ == "__main__":
    main()

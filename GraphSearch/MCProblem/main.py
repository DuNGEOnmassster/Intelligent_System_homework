import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="MC Problem")

    parser.add_argument("--N", default=3,
                        help="Number of Missionaries and Cannibals")
    parser.add_argument("--K", default=2,
                        help="Maximum passenger number that the boat is able to carry")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
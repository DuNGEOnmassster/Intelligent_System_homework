import argparse
from dataclasses import dataclass

def parse_args():
    parser = argparse.ArgumentParser(description="MC Problem")

    parser.add_argument("--N", default=3,
                        help="Number of Missionaries and Cannibals")
    parser.add_argument("--K", default=2,
                        help="Maximum passenger number that the boat is able to carry")

    return parser.parse_args()


@dataclass
class S:
    m: int  # M in left side
    c: int  # C in left side
    b: bool # boat side, 0 equals to left and 1 equals to right


def get_init():
    start_state = S(3,3,1)
    target_state = S(0,0,0)
    return start_state, target_state

if __name__ == "__main__":
    args = parse_args()
    print(S(3,3,1))

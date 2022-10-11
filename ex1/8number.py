import numpy as np
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Animal identify system")

    parser.add_argument("-t","--test", default="./dataset/test.txt",
                        help="test data sentense for identification")
    parser.add_argument("--extend", default=False,
                        help="whether use extend rules or not, default False")
    parser.add_argument("--extend_rules", default="./dataset/extend_rules.txt",
                        help="input file to extend rules.")

    return parser.parse_args()


def init_board():
    return np.array([i for i in range(9)]).reshape([3,3])


def get_target():
    target = [0, 1, 2, 7, 8, 3, 6, 5, 4]
    return np.array(target).reshape([3,3])


if __name__ == "__main__":
    start = init_board()
    target = get_target()
    print(f"start:\n{start}\ntarget:\n{target}")
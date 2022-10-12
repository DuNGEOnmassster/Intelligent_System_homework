import numpy as np
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Animal identify system")

    parser.add_argument("--diy_start", default=False,
                        help="judge whether to diy start 8 number map or not, default with False")
    parser.add_argument("--start", default=[i for i in range(9)],
                        help="design the start 8 number map")
    parser.add_argument("--diy_target", default=False,
                        help="judge whether to diy target 8 number map or not, default with False")
    parser.add_argument("--target", default=[0, 1, 2, 7, 8, 3, 6, 5, 4],
                        help="design the start 8 number map")

    return parser.parse_args()


def get_start(args):
    if not args.diy_start:
        return np.array(args.start).reshape([3,3])
    else:
        arr = []
        for i in range(9):
            arr.append(input(f"input number in start map {i}/9"))
            return np.array(args.arr).reshape([3,3])


def get_target(args):
    if not args.diy_target:
        return np.array(args.target).reshape([3,3])
    else:
        arr = []
        for i in range(9):
            arr.append(input(f"input number in targer map {i}/9"))
            return np.array(args.arr).reshape([3,3])


def init():
    args = parse_args()
    start = get_start(args)
    target = get_target(args)
    print(f"start:\n{start}\ntarget:\n{target}")
    return start, target


def get_differ(now, target):
    cnt = 0
    for i in range(9):
        if now[i//3][i%3] == target[i//3][i%3]:
            cnt = cnt + 1
    return cnt


def process(start, target):
    open_list = []


if __name__ == "__main__":
    start,target = init()
    print(get_differ(start, target))
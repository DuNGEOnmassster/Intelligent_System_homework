import numpy as np
import argparse
from utils.common import number_Node

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


def get_best_extend(extend_list):
    # f = h + g, get the smallest f
    min_f = 10086
    for item in extend_list:
        if (item.h + item.g) < min_f:
            min_f = item.h + item.g
            goal = item

    return goal


def get_extend(now_node, close_list):
    extend_list = []
    # find the position of zero
    zero_index = np.where(now_node.map == 0)[0][0]
    row = zero_index // 3
    col = zero_index % 3
    # find the potential extend position
    
    # if not in close list, add into close list and extend list

    return extend_list
    


def process(start, target):
    # initialize list and node
    open_list = []
    close_list = set()
    start_node = number_Node(start, 0, get_differ(start,target), None)
    open_list.append(start_node)
    close_list.add(start_node)
    pre_node = start_node
    # while open list not empty
    while open_list:
        print("not empty")
        open_list.pop()
        extend_list = get_extend(pre_node, open_list)
        new_node = get_best_extend(extend_list)
        new_node.f = pre_node.f + 1
        open_list.append(new_node)
        



if __name__ == "__main__":
    start,target = init()
    process(start, target)
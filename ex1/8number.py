import numpy as np
import argparse
from utils.common import *

def parse_args():
    parser = argparse.ArgumentParser(description="Animal identify system")

    parser.add_argument("--diy_start", default=False,
                        help="judge whether to diy start 8 number map or not, default with False")
    parser.add_argument("--start", default=[i for i in range(9)],
                        help="design the start 8 number map")
    parser.add_argument("--diy_target", default=False,
                        help="judge whether to diy target 8 number map or not, default with False")
    parser.add_argument("--target", default=[1, 5, 3, 2, 4, 6, 7, 0, 8],
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


def get_string_map(map):
    num_list = [str(i) for i in range(9)]
    str_map = ''
    for i in str(map):
        if i in num_list:
            str_map += i
    return str_map


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
    goal = None
    for item in extend_list:
        if (item.h + item.g) < min_f:
            min_f = item.h + item.g
            goal = item

    return goal


def get_extend(now_node: number_Node, close_list):
    now_map = now_node.map.copy()
    extend_rules = {0:[1], 1:[0,2], 2:[1]}
    extend_list = []

    # find the position of zero
    zero_index = np.where(now_node.map == 0)[0][0]
    row = zero_index // 3
    col = zero_index % 3

    # find the potential extend position
    potential_extend = [[row, i] for i in extend_rules[col]]
    for j in extend_rules[row]:
        potential_extend.append([j, col])
    print(f"potential_extend = {potential_extend}")

    # create new extend map for every potential extend position
    for extend_point in potential_extend:
        extend_node = number_Node(now_node.map.copy(), now_node.h+1, now_node.g, now_node)
        extend_node.map[row][col] = extend_node.map[extend_point[0]][extend_point[1]]
        extend_node.map[extend_point[0]][extend_point[1]] = 0
        print(f"extend node:\n{extend_node.map}")

        # if not in close list, add into close list and extend list
        extend_map = get_string_map(extend_node.map)
        if extend_map not in close_list:
            close_list.append(get_string_map(extend_node.map))
            extend_list.append(extend_node)
            
    return extend_list
    

def process(start, target):
    # initialize list and node
    open_list = []
    close_list = []
    start_node = number_Node(start, 0, get_differ(start,target), None)
    open_list.append(start_node)
    close_list.append(get_string_map(start_node.map))
    pre_node = start_node

    # while open list not empty
    while open_list:
        print("not empty")
        open_list.pop()
        extend_list = get_extend(pre_node, open_list)
        print(f"extend_list:\n{extend_list}")
        new_node = get_best_extend(extend_list)
        if new_node == None:
            print("search failed")
        else:
            if new_node.g == 0:
                print(f"achieve target!")
                break
            else:
                pre_node = new_node
                new_node.h = pre_node.h + 1
                open_list.append(new_node)
        

if __name__ == "__main__":
    start,target = init()
    # process(start, target)
    print(get_string_map(start))
    print(get_string_map(target))
    opened = [start]
    closed = []
    Fn = {}  # 状态对应的估价函数值 f(n)  =  g(n) + h(n)
    Gn = {}  # 初始结点到当前结点n的实际代价，即路径长度
    parent = {}  # 用来存储状态对应的父结点
    
    result = a_star(get_string_map(start), get_string_map(target), parent, Gn, Fn)

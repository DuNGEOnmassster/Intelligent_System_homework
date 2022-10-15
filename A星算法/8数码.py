import sys

import numpy as np
import common


class node:
    def __init__(self, map, g, h, pre=None, last_step_int=None):
        self.map = map
        self.g = g
        self.h = h
        self.pre = pre
        self.last_step = last_step_int


map_temp = np.zeros((3, 3), dtype=int)
print(map_temp)
# print("输入初始状态，每个数字间")
# map_input = input("第一行：")
for i in range(3):
    for j in range(3):
        map_temp[i][j] = input(f"第{i+1}行{j+1}列：")

# 转换为numpy矩阵
# map_temp = np.array([[8, 3, 2], [4, 0, 1], [6, 7, 5]])
map_target = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])

solvable = common.is_solvable(map_temp)
if solvable % 2 == 0:
    print("无解")
    sys.exit(-1)

open_dict = {}
close_dict = set()
h = common.h(map_temp, map_target)
open_dict[common.get_map_str(map_temp)] = node(map_temp, 0, h)
open_dict["meta"] = [[common.get_map_str(map_temp), h]]

# 大循环，open表非空
while len(open_dict) is not 0:
    index_str0 = open_dict["meta"][0][0]
    # index_str0为字典第一个元素
    # 取出首元素做扩展（默认首元素为f最小）
    old_node = open_dict.pop(index_str0)
    close_dict.add(index_str0)
    open_dict["meta"].pop(0)
    if common.get_map_str(old_node.map) == "123804765":
        while old_node is not None:
            print(f"第{old_node.g}步：")
            common.find_step(old_node.last_step)
            print("现在形状：\n", old_node.map)
            old_node = old_node.pre
        sys.exit("找到解")
    x0, y0 = np.where(old_node.map == 0)
    for i in range(4):
        new_map = common.move(old_node.map, i, x0[0], y0[0])
        if new_map is not None:
            new_map_str = common.get_map_str(new_map)
            new_map_g = old_node.g+1
            new_map_h = common.h(new_map, map_target)
            if new_map_str in open_dict:
                # 该新节点出现过，则尝试更新
                if new_map_h+new_map_g < open_dict[new_map_str].g+open_dict[new_map_str].h:
                    open_dict[new_map_str].g = new_map_g
                    open_dict[new_map_str].h = new_map_h
            else:
                # 没出现过且不在close——dict，则添加进open_dict
                if new_map_str not in close_dict:
                    open_dict[new_map_str] = node(new_map, new_map_g, new_map_h, old_node, i)
                    # meta元组做插入排序
                    length = len(open_dict["meta"])
                    inserted = False
                    for index in range(length):
                        if new_map_g + new_map_h < open_dict["meta"][index][1]:
                            open_dict["meta"].insert(index, [new_map_str, new_map_g + new_map_h])
                            inserted = True
                            break
                    if not inserted:
                        open_dict["meta"].insert(length, [new_map_str, new_map_g + new_map_h])
                        # print(open_dict["meta"])

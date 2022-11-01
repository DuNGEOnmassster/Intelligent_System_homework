import numpy as np
from dataclasses import dataclass

@dataclass
class number_Node:
    map: list # now map
    h: int  # price already paid
    g: int  # differ bewteen target
    pre_map: list # pre map


def reversenum(node):
    """计算状态对应的逆序数,奇偶性一致则有解"""
    Sum = 0
    for i in range(1,9):
        num = 0
        for j in range(0,i):
          if node[j]>node[i] and node[i] != '0':
              num = num + 1
        Sum += num
    return Sum


def a_star(start, goal, parent, Gn, Fn):
    if start == goal:
        print("初始状态和目标状态一致！")
        
    # 判断从初始状态是否可以达到目标状态
    if (reversenum(start)%2) != (reversenum(goal)%2):
        print("该目标状态不可达！")
        return None
        
    else:
        parent[start] = -1                # 初始结点的父结点存储为-1
        Gn[start] = 0                     # 初始结点的g(n)为0
        Fn[start] = Gn[start] + Hn(start)  # 计算初始结点的估价函数值 f(n)  =  g(n) + h(n)

        while opened:
            current = select_min(opened)  # 选择估价函数值最小的状态
            del Fn[current]              # 对代价清零
            opened.remove(current)       # 将要遍历的结点取出opened表

            if current == goal:
                break
                
            if current not in closed:
                closed.append(current)     # 存入closed表 
                Tnode = expand_node(current)    # 扩展子结点.用来遍历节点n所有的邻近节点
                print(f"Tnode =\n{Tnode}")
                for node in Tnode:
                    # 如果子结点在opened和closed表中都未出现，则存入opened表
                    # 并求出对应的估价函数值
                    if node not in opened and node not in closed:
                        Gn[node] = Gn[current]+1
                        Fn[node] = Gn[node]+Hn(node)
                        parent[node] = current
                        opened.append(node)
                    else:
                        # 若子结点已经在opened表中，则判断估价函数值更小的一个路径
                        # 同时改变parent字典和Fn字典中的值
                        if node in opened:
                            fn = Gn[current] + 1 + Hn(node)
                            if fn < Fn[node]:
                                Fn[node] = fn
                                parent[node] = current

        result = []  # 用来存放路径
        result.append(current)
        
        while parent[current] != -1:  # 根据parent字典中存储的父结点提取路径中的结点
            current  = parent[current]
            result.append(current)
        result.reverse()  # 逆序即为运行时的过程
        return result
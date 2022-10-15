# 开发时间 2022/9/21 11:28
import numpy as np

def find_step(last_step_int):
    if last_step_int == 0:
        print("上移")
    elif last_step_int == 1:
        print("右移")
    elif last_step_int == 2:
        print("下移")
    elif last_step_int == 3:
        print("左移")
    else:
        print("初始状态：")
    return


def is_solvable(start_map):
    reverse_sum = 0
    nums = []
    for row in start_map:
        for num in row:
            if num != 0: nums.append(num)
    # print(nums)
    for index in range(8):
        for num in nums[index+1:]:
            if num < nums[index]: reverse_sum += 1
    # print(reverse_sum)
    return reverse_sum


def get_map_str(map):
    ans = ""
    for row in map:
        for num in row:
            ans += str(num)
    return ans


def move(map, direction, x0, y0):
    x, y = x0, y0
    point = np.copy(map)
    if direction == 0: # 上移
        if x == 0:
            # print("不能上移")
            return
        point[x][y] = point[x-1][y]
        point[x-1][y] = 0
        return point
    if direction == 1: # 右移
        if y == 2:
            # print("不能右移")
            return
        point[x][y] = point[x][y+1]
        point[x][y+1] = 0
        return point
    if direction == 2: # 下移
        if x == 2:
            # print("不能下移")
            return
        point[x][y] = point[x+1][y]
        point[x+1][y] = 0
        return point
    if direction == 3: # 左移
        if y == 0:
            # print("不能左移")
            return
        point[x][y] = point[x][y-1]
        point[x][y-1] = 0
        return point


def manhattan(x1, y1, x2, y2):
    distance = abs(y2-y1)+abs(x2-x1)
    return int(distance)


def h(map_now, map_target):
    sum = 0
    for i in range(1, 9):
        x_now, y_now = np.where(map_now == i)
        x_target, y_target = np.where(map_target == i)
        sum += manhattan(x_now[0], y_now[0], x_target[0], y_target[0])
    return sum
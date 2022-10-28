from cmath import sqrt
import numpy as np
from dataclasses import dataclass

@dataclass
class monkey_sta:
    x: int
    y: int
    road: int

@dataclass
class box_sta:
    x: int
    y: int

@dataclass
class banana_sta:
    x: int
    y: int

@dataclass
class valid:
    monkey: monkey_sta
    box: box_sta
    banana: banana_sta
    climb: bool
    reach_banana: bool


def is_vaild(valid_point):
    return valid_point.reach_banana


def init(valid_point, monkey_start, box_start, banana_start):
    valid_point.monkey = monkey_start
    valid_point.box = box_start
    valid_point.banana = banana_start
    valid_point.monkey.road = 0


def Manhatta_distance(a, b):
    return sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2))


def A_star(start, target, now):
    hx = now.road
    gx = Manhatta_distance(now, target)

    
    
if __name__ == "__main__":
    valid_point = valid()
    monkey_start = monkey_sta(0, 0)
    box_start = box_sta(5, 5)
    banana_start = banana_sta(4, 4)
    init(valid_point, monkey_start, box_start, banana_start)
    



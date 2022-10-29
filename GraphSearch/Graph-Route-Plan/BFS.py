# Use BFS algorithm to solve easy traffic cost problem
from dataclasses import dataclass
import heapq as hq


@dataclass
class City:
    name: str
    cost2parent: int
    parent: str


def bfs(traffic_map, start, target):
    visited = []
    queue = []
    parent = {}

    visited.append(start)
    queue.append(start)

    while queue:
        m = queue.pop(0)
        print(m)

        for neighbour in traffic_map[m]:
            print(f"neighbour = {neighbour}")
            if neighbour not in visited:
                visited.append(neighbour)
                hq.heappush(queue, neighbour)
    print(end="\n")

if __name__ == "__main__":
    graph = {
        "A" : {"B": 1, "C": 3},
        "B" : {"A": 1, "D": 3, "E": 5},
        "C" : {"A": 3, "H": 2},
        "D" : {"B": 3, "F": 4},
        "E" : {"B": 5, "G": 2, "H": 2},
        "F" : {"D": 4, "G": 1, "I": 3},
        "G" : {"E": 2, "F": 1, "I": 2, "J": 1},
        "H" : {"C": 2, "E": 2, "K": 3},
        "I" : {"F": 3, "G": 2, "L": 3},
        "J" : {"G": 1, "K": 2, "L": 1},
        "K" : {"H": 3, "J": 2},
        "L" : {"I": 3, "J": 1},
    }
    city_start = "A"
    city_target = "L"

    bfs(graph, city_start, city_target)


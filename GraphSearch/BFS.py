# Use BFS algorithm to solve easy traffic cost problem
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
visited = []
queue = []

def bfs(visited, traffic_map, city):
    visited.append(city)
    queue.append(city)

    while queue:
        m = queue.pop(0)
        print(m, end = " ")

        for neighbour in traffic_map[m]:
            print(f"neighbour = {neighbour}")
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    print(end="\n")

bfs(visited=visited, traffic_map=graph, city="A")

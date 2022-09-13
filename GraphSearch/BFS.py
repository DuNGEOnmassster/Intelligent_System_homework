# Use BFS algorithm to solve easy traffic cost problem
graph = {
    "A" : {"B": 1, "C": 3},
    "B" : {"A": 1, "D": 3, "E": 5},
    "C" : {"A": 3, "H": 2},
    "D" : {"B": 3, "F": 4},
    "E" : {"B": 5, "G": 2, "H":}

}
visited = []
queue = []

def bfs(visited, traffic_map, city):
    visited.append(city)
    queue.append(city)

    while queue:
        m = queue.pop(0)

        for neighbour in traffic_map[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)



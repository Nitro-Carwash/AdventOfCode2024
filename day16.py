import heapq

x_offsets = [-1, 0, 1, 0]
y_offsets = [0, -1, 0, 1]


def load_input():
    map = []
    start = (0, 0)
    end = (0,0)
    with open('in16', 'r') as in_stream:
        line = in_stream.readline().strip()
        while len(line) > 0:
            map.append([t for t in line])
            if 'S' in line:
                start = (line.find('S'), len(map) - 1)
            if 'E' in line:
                end = (line.find('E'), len(map) - 1)

            line = in_stream.readline().strip()

        return map, start, end


def forward_search(map, start):
    visited = {
        (start[0], start[1], 2): 0
    }
    pq = [(0, start[0], start[1], 2)]

    while len(pq) > 0:
        cost, x, y, direction = heapq.heappop(pq)

        for d in [i for i in range(len(x_offsets)) if i != (direction + 2) % 4]:
            nx = x + x_offsets[d] if d == direction else x
            ny = y + y_offsets[d] if d == direction else y

            if map[ny][nx] == '#' or (nx, ny, d) in visited:
                continue

            ncost = cost + 1 if d == direction else 1000 + cost
            visited[(nx, ny, d)] = ncost
            heapq.heappush(pq, (ncost, nx, ny, d))

    return visited


def backward_search(map, fwd_search_visited, target_state, target_value):
    target_state = (target_state[0], target_state[1], (target_state[2] + 2) % 4)
    visited = {
        target_state: 0
    }
    pq = [(0, target_state[0], target_state[1], target_state[2])]
    optimal_tiles = set()

    while len(pq) > 0:
        cost, x, y, direction = heapq.heappop(pq)
        key = (x, y, (direction + 2) % 4)

        if key in fwd_search_visited and fwd_search_visited[key] + cost == target_value:
            optimal_tiles.add((x, y))

        for d in [i for i in range(len(x_offsets)) if i != (direction + 2) % 4]:
            nx = x + x_offsets[d] if d == direction else x
            ny = y + y_offsets[d] if d == direction else y

            if map[ny][nx] == '#' or (nx, ny, d) in visited:
                continue

            ncost = cost + 1 if d == direction else 1000 + cost
            visited[(nx, ny, d)] = ncost
            heapq.heappush(pq, (ncost, nx, ny, d))


    return optimal_tiles


def solve():
    map, start, end = load_input()
    visited = forward_search(map, start)
    target_cost = [v for k, v in visited.items() if k[0] == end[0] and k[1] == end[1]][0]
    target_state = [k for k, v in visited.items() if k[0] == end[0] and k[1] == end[1]][0]
    print(f"Score for an optimal path: {target_cost}")
    print(f"Number of tiles on all optimal paths: {len(backward_search(map, visited, target_state, target_cost))}")


solve()
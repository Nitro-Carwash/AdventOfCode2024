x_offsets = [-1, 0, 1, 0]
y_offsets = [0, -1, 0, 1]


def load_input():
    with open('in10', 'r') as in_stream:
        return [[int(t) for t in line.strip()] for line in in_stream.readlines()]


def sum_trailhead(trail_map, use_rankings=False):
    total = 0
    for y in range(len(trail_map)):
        for x in range(len(trail_map[0])):
            if trail_map[y][x] == 0:
                total += calculate_rating_for_trailhead(trail_map, x, y) if use_rankings else calculate_score_for_trailhead(trail_map, x, y)

    return total


def calculate_score_for_trailhead(trail_map, x_start: int, y_start: int):
    expanded = [[False for _ in range(len(trail_map[0]))] for _ in range(len(trail_map))]
    peaks_reached = 0
    bfs = [(x_start, y_start)]
    expanded[y_start][x_start] = True
    while len(bfs) > 0:
        x, y = bfs.pop(0)

        if trail_map[y][x] == 9:
            peaks_reached += 1
            continue

        current_height = trail_map[y][x]
        for i in range(len(x_offsets)):
            nx = x + x_offsets[i]
            ny = y + y_offsets[i]
            if 0 <= nx < len(trail_map[0]) and 0 <= ny < len(trail_map) and not expanded[ny][nx] and trail_map[ny][nx] == current_height + 1:
                expanded[ny][nx] = True
                bfs.append((nx, ny))

    return peaks_reached


def calculate_rating_for_trailhead(trail_map, x_start: int, y_start: int):
    ratings = [[0 for _ in range(len(trail_map[0]))] for _ in range(len(trail_map))]
    peaks_reached = set()
    bfs = [(x_start, y_start)]
    ratings[y_start][x_start] = 1
    while len(bfs) > 0:
        x, y = bfs.pop(0)

        if trail_map[y][x] == 9:
            peaks_reached.add((x, y))
            continue

        current_height = trail_map[y][x]
        for i in range(len(x_offsets)):
            nx = x + x_offsets[i]
            ny = y + y_offsets[i]
            if 0 <= nx < len(trail_map[0]) and 0 <= ny < len(trail_map) and trail_map[ny][nx] == current_height + 1:
                ratings[ny][nx] += 1
                bfs.append((nx, ny))

    return sum([ratings[y][x] for x, y in peaks_reached])



trail_map = load_input()
print(f"Total trailhead score: {sum_trailhead(trail_map)}")
print(f"Total trailhead rating: {sum_trailhead(trail_map, use_rankings=True)}")

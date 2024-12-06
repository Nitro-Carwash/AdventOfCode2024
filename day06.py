directions = ["^", ">", "v", "<"]
offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def load_input():
    with open('in06', 'r') as in_stream:
        return [list(line.strip()) for line in in_stream.readlines()]


def count_path(map, x, y, direction_index, seen, look_for_cycle=False):
    depth_limit = 1000000
    depth = 0

    while depth < depth_limit:
        depth += 1
        if y < 0 or y >= len(map) or x < 0 or x >= len(map[0]):
            return False

        direction = offsets[direction_index]
        if map[y][x] == "#":
            # Backtrack one, rotate, and try again
            x = x - direction[0]
            y = y - direction[1]
            direction_index = (direction_index + 1) % len(directions)
        else:
            tile = (x, y, direction_index) if look_for_cycle else (x, y)
            if look_for_cycle and tile in seen:
                return True
            seen.add(tile)
            x = x + direction[0]
            y = y + direction[1]

    return False


def count_potential_cycles(map, sx, sy, direction_index, seen):
    cycle_count = 0
    for x, y in seen:
        if x == sx and y == sy:
            continue

        map[y][x] = "#"
        cycle_count += 1 if count_path(map, sx, sy, direction_index, set(), look_for_cycle=True) else 0
        map[y][x] = "."

    return cycle_count


map = load_input()

start_x, start_y = [(x, y) for x in range(0, len(map[0])) for y in range(len(map)) if map[y][x] in directions][0]
guard_symbol = map[start_y][start_x]
start_direction_index = directions.index(guard_symbol)
start_offset = offsets[start_direction_index]

explored = set()
count_path(map, start_x, start_y, start_direction_index, explored)
print(f"Number of tiles contained within the guard's patrol route: {len(explored)}")
print(f"Number of potential cycles in the guard's patrol route: {count_potential_cycles(map, start_x, start_y, start_direction_index, explored)}")

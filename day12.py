x_offsets = [-1, 0, 1, 0]
y_offsets = [0, -1, 0, 1]


def load_input():
    with open('in12', 'r') as in_stream:
        return [[p for p in line.strip()] for line in in_stream.readlines()]


def sum_patch_costs(farm, use_discount=False):
    total = 0
    seen = [[False for _ in range(len(farm[0]))] for _ in range(len(farm))]
    for y in range(len(farm)):
        for x in range(len(farm[0])):
            if not seen[y][x]:
                total += calculate_price_for_patch(farm, x, y, farm[y][x], seen, use_discount)

    return total


def calculate_price_for_patch(farm, x_start: int, y_start: int, plant_type: str, seen, use_bulk_discount=False):
    bfs = [(x_start, y_start)]
    seen[y_start][x_start] = True
    area = 1
    if use_bulk_discount:
        sides = [[[False, False, False, False] for _ in range(len(farm[0]))] for _ in range(len(farm))]
    perimeter = 0
    while len(bfs) > 0:
        x, y = bfs.pop(0)

        for direction in range(len(x_offsets)):
            nx = x + x_offsets[direction]
            ny = y + y_offsets[direction]
            if nx < 0 or nx >= len(farm[0]) or ny < 0 or ny >= len(farm) or farm[ny][nx] != plant_type:
                if use_bulk_discount:
                    perimeter += 1 if add_side(sides, direction, x, y) else 0
                else:
                    perimeter += 1
            elif not seen[ny][nx]:
                area += 1
                seen[ny][nx] = True
                bfs.append((nx, ny))

    return area * perimeter


# Add a side record to the data structure, and return true if its neighbors have not seen this side (first time)
# The sides data structure is just a mxn 2d array with 4 boolean entries in each cell.
# Each entry represents whether this cell (IN the matching farm patch) has already seen a transition out of the farm
# patch (a fence) in this cardinal direction (in whatever order x_offset and y_offset take us - it's arbitrary)
# Whenever we find a fence, we check the orthogonal neighbor cells to this cell's transition, and check if they
# have also seen this transition.  If not, then this is a new side.  Since the calling function is doing a BFS, there
# should never be a situation where we will later need to join two side segments - not that I've proven this ;)
def add_side(sides, direction: int, x: int, y: int):
    sides[y][x][direction] = True
    for i in [1, 3]:
        nx = x + x_offsets[(direction + i) % len(x_offsets)]
        ny = y + y_offsets[(direction + i) % len(y_offsets)]
        if nx < 0 or nx >= len(sides[0]) or ny < 0 or ny >= len(sides):
            continue
        if sides[ny][nx][direction]:
            return False

    return True


farm_map = load_input()
print(f"Total cost for fencing without bulk discount: {sum_patch_costs(farm_map)}")
print(f"Total cost for fencing with bulk discount: {sum_patch_costs(farm_map, use_discount=True)}")

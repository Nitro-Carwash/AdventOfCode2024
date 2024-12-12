x_offsets = [-1, 0, 1, 0]
y_offsets = [0, -1, 0, 1]


def load_input():
    with open('in12', 'r') as in_stream:
        return [[p for p in line.strip()] for line in in_stream.readlines()]


def sum_patch_costs(farm, use_discount=False):
    total = 0
    seen: set[tuple[int, int]] = set()
    for y in range(len(farm)):
        for x in range(len(farm[0])):
            if (x, y) not in seen:
                total += calculate_price_for_patch(farm, x, y, farm[y][x], seen, use_discount)

    return total


def calculate_price_for_patch(farm, x_start: int, y_start: int, plant_type: str, seen, use_bulk_discount=False):
    bfs = [(x_start, y_start)]
    seen.add((x_start, y_start))
    area = 1
    if use_bulk_discount:
        sides: set[tuple[int, int, int]] = set()
    perimeter = 0
    while len(bfs) > 0:
        x, y = bfs.pop(0)

        for direction in range(len(x_offsets)):
            nx = x + x_offsets[direction]
            ny = y + y_offsets[direction]
            if nx < 0 or nx >= len(farm[0]) or ny < 0 or ny >= len(farm) or farm[ny][nx] != plant_type:
                if use_bulk_discount:
                    perimeter += add_side(farm, sides, direction, x, y)
                else:
                    perimeter += 1
            elif (nx, ny) not in seen:
                area += 1
                seen.add((nx, ny))
                bfs.append((nx, ny))

    return area * perimeter


# Add a side record to the data structure, and return a delta for to adjust the total accordingly
# Each entry of sides represents whether this cell (IN the matching farm patch) has already seen a transition out of the
# farm patch (a fence) in this cardinal direction (in whatever order x_offset and y_offset take us - it's arbitrary)
# Whenever we find a fence, we check the orthogonal neighbor cells to this cell's transition, and check if they
# have also seen this transition.  If not, then this is a new side.  If one of them has seen this transition, then it's
# not new.  If BOTH of them have seen this transition then there's a problem - at some point these two sides appeared
# to have been disjoint and so the global total is too high.  We return -1 in this case to adjust it back.
def add_side(farm, sides, direction: int, x: int, y: int):
    sides.add((x, y, direction))
    orthogonal_count = 0
    for i in [1, 3]:
        nx = x + x_offsets[(direction + i) % len(x_offsets)]
        ny = y + y_offsets[(direction + i) % len(y_offsets)]
        if nx < 0 or nx >= len(farm[0]) or ny < 0 or ny >= len(farm):
            continue
        if (nx, ny, direction) in sides:
            orthogonal_count += 1

    return -1 if orthogonal_count == 2 else (1 - orthogonal_count)


farm_map = load_input()
print(f"Total cost for fencing without bulk discount: {sum_patch_costs(farm_map)}")
print(f"Total cost for fencing with bulk discount: {sum_patch_costs(farm_map, use_discount=True)}")

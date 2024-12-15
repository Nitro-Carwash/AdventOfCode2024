x_offsets = [-1, 0, 1, 0]
y_offsets = [0, -1, 0, 1]
dir_to_offset_idx = {'<': 0, '^': 1, '>': 2, 'v': 3}
wide_replacements = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}


def load_input(wide=False):
    map = []
    start = (0, 0)
    with open('in15', 'r') as in_stream:
        line = in_stream.readline().strip()
        while len(line) > 0:
            if wide:
                line = "".join([t for c in line for t in wide_replacements[c]])

            map.append([t for t in line])
            if '@' in line:
                start = (line.find('@'), len(map) - 1)

            line = in_stream.readline().strip()

        directions = [d for line in in_stream.readlines() for d in line.strip()]

        return map, directions, start


def simulate_robot(map, directions, start):
    x, y = start
    for d in directions:
        d_idx = dir_to_offset_idx[d]
        dx = x_offsets[d_idx]
        dy = y_offsets[d_idx]

        if simulate_movement(map, dx, dy, x + dx, y + dy, '@'):
            map[y][x] = '.'
            x, y = x + dx, y + dy


def simulate_movement(map, dx, dy, x, y, replace_with):
    if map[y][x] == '#':
        return False

    if map[y][x] == '.':
        map[y][x] = replace_with
        return True

    if map[y][x] in ['O', '[', ']']:
        if simulate_movement(map, dx, dy, x + dx, y + dy, map[y][x]):
            map[y][x] = replace_with
            return True
        return False


def simulate_movement2(map, dy, x, y):
        # Box2 is just a pair of tuples for the two coordinates that make up a box, with some helper functions
        class Box2:
            def __init__(self, x, y, tile):
                self.x = x if tile == '[' else x - 1
                self.x2 = self.x + 1
                self.idx = 0
                self.y = y

            def __iter__(self):
                self.idx = 0
                return self

            def __next__(self):
                if self.idx > 1:
                    raise StopIteration

                val = (self.x, self.y, '[') if self.idx == 0 else (self.x2, self.y, ']')
                self.idx += 1
                return val

            def __hash__(self):
                return hash((self.x, self.y)) + hash((self.x2, self.y))

            def __eq__(self, other):
                return self.x == other.x and self.x2 == other.x2 and self.y == other.y

        # Do a BFS over the boxes connected to the first box that will be pushed if the starting box is pushed.
        # Return false immediately if any of these boxes run into a wall.
        # If we make it through the BFS without returning false, then this is a valid push.
        # Keep track of all the boxes we touch during this process (ensuring no duplicates) so that we can actually move
        # them at the end.
        bfs = [Box2(x, y + dy, map[y + dy][x])]
        seen_ordered = []
        seen = set()
        while len(bfs) > 0:
            box = bfs.pop(0)
            if box in seen:
                continue

            seen_ordered.append(box)
            seen.add(box)

            for nx, ny, _ in box:
                next_tile = map[ny+dy][nx]
                if next_tile == '#':
                    return False
                if next_tile in ['[', ']']:
                    bfs.append(Box2(nx, ny + dy, next_tile))
                    # If this is the left tile of a box, the next iteration (if there even is one) is redundant
                    if next_tile == '[':
                        break

        # The entire bfs was successful so let's move some boxes!!!!!
        # Iterate backwards since the BFS will find boxes in ascending order of distance from the first box
        for box in reversed(seen_ordered):
            for x, y, tile in box:
                map[y][x] = '.'
                map[y + dy][x] = tile

        return True

def simulate_robot2(map, directions, start):
    x, y = start
    for d in directions:
        d_idx = dir_to_offset_idx[d]
        dx = x_offsets[d_idx]
        dy = y_offsets[d_idx]

        # Exactly the same as in part 1 if moving along the x-axis, or an empty tile
        if dy == 0 or map[dy + y][dx + x] == '.':
            if simulate_movement(map, dx, dy, x + dx, y + dy, '@'):
                map[y][x] = '.'
                x, y = x + dx, y + dy
        elif map[dy + y][dx + x] != '#':
            # If we're running into a box on the y-axis, we need to use different logic
            if simulate_movement2(map, dy, x, y):
                map[y][x] = '.'
                map[dy + y][dx + x] = '@'
                x, y = x + dx, y + dy


map, directions, start = load_input()
simulate_robot(map, directions, start)
gps_sum = sum([100*y + x for y, row in enumerate(map) for x, t in enumerate(row) if t == 'O'])
print(f"Sum of GPS coordinates after robot finishes traipsing: {gps_sum}")

map, directions, start = load_input(True)
simulate_robot2(map, directions, start)
gps_sum = sum([100*y + x for y, row in enumerate(map) for x, t in enumerate(row) if t == '['])
print(f"Sum of GPS coordinates after robot finishes traipsing in a WIDE warehouse: {gps_sum}")

empty_tile = '.'


def load_input():
    with open('in08', 'r') as in_stream:
        return [list(line.strip()) for line in in_stream.readlines()]


def load_tower_positions(map):
    freq_to_positions = {}
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] != empty_tile:
                if map[y][x] not in freq_to_positions:
                    freq_to_positions[map[y][x]] = []
                freq_to_positions[map[y][x]].append((x, y))

    return freq_to_positions


def find_antinodes(map, use_resonant_harmonics=False):
    freq_to_positions = load_tower_positions(map)
    antinodes = set()
    for frequency in freq_to_positions.keys():
        positions = freq_to_positions[frequency]
        for i in range(0, len(positions)):
            position = positions[i]

            for other_position in positions[:i] + positions[i+1:]:
                diff = (position[0] - other_position[0], position[1] - other_position[1])

                if use_resonant_harmonics:
                    antinode_position = position
                    while is_position_in_map(map, antinode_position):
                        antinodes.add(antinode_position)
                        antinode_position = (antinode_position[0] + diff[0], antinode_position[1] + diff[1])
                else:
                    antinode_position = (position[0] + diff[0], position[1] + diff[1])
                    if is_position_in_map(map, antinode_position):
                        antinodes.add(antinode_position)

    return antinodes


def is_position_in_map(map, position):
    return 0 <= position[1] < len(map) and 0 <= position[0] < len(map[0])


map = load_input()
antinodes = find_antinodes(map)
print(f"Unique antinodes found: {len(antinodes)}")
antinodes = find_antinodes(map, use_resonant_harmonics=True)
print(f"Unique antinodes found when remembering to account for resonant harmonics: {len(antinodes)}")

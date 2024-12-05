import re

search_string_regular = "XMAS"
search_string_X = "MAS"
pivot_depth = 1
dxy_all = [-1, 0, 1]
dxy_diagonal = [-1, 1]


def load_input():
    with open('in04', 'r') as in_stream:
        return [list(line.strip()) for line in in_stream.readlines()]


def word_search_from(grid, search_string, x, y, dx, dy, i=0, pivot=None):
    if i >= len(search_string):
        return True, pivot

    if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
        return False, -1

    if grid[y][x] == search_string[i]:
        if i == pivot_depth:
            pivot = (x, y)
        return word_search_from(grid, search_string, x + dx, y + dy, dx, dy, i + 1, pivot)

    return False, -1


def word_search(grid, search_string, x_mode=False):
    word_found_count = 0
    found_pivots = set()
    dxy = dxy_diagonal if x_mode else dxy_all

    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            for dy in dxy:
                for dx in dxy:
                    found, pivot = word_search_from(grid, search_string, x, y, dx, dy)
                    if found:
                        if not x_mode:
                            word_found_count += 1
                        else:
                            if pivot in found_pivots:
                                word_found_count += 1
                            else:
                                found_pivots.add(pivot)

    return word_found_count


grid = load_input()
print(f"occurrences of {search_string_regular}: {word_search(grid, search_string_regular)}")
print(f"occurrences of {search_string_X} in only crosses: {word_search(grid, search_string_X, x_mode=True)}")

import re


def load_input():
    with open('in03', 'r') as in_stream:
        return ''.join([line for line in in_stream.readlines()])


def sum_muls(line):
    groups = re.findall(r"mul\((\d\d?\d?),(\d\d?\d?)\)", line)
    return sum([int(group[0]) * int(group[1]) for group in groups])


def sum_muls_with_conditionals(line):
    enabled = True
    conditional_memory = ''
    i = 0
    search_limit = 0
    while i < len(line) and search_limit < 10000:
        search_limit += 1
        search_string = "don't()" if enabled else "do()"
        end_of_current_instruction = line.find(search_string, i)
        if end_of_current_instruction == -1:
            end_of_current_instruction = len(line)

        if enabled:
            conditional_memory += (line[i:end_of_current_instruction])
        i = end_of_current_instruction + len(search_string)
        enabled = not enabled

    return sum_muls(conditional_memory)


memory = load_input()
print(f"sum of intact multiply operations: {sum_muls(memory)}")
print(f"sum of intact multiply operations with conditionals: {sum_muls_with_conditionals(memory)}")

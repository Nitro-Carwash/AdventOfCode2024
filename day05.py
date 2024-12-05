import math


def load_input():
    rules = []
    updates = []
    with open('in05', 'r') as in_stream:
        line = in_stream.readline().strip()
        # Until we get to the updates
        while len(line) > 0:
            rules.append([int(r) for r in line.split("|")])
            line = in_stream.readline().strip()

        line = in_stream.readline().strip()
        while len(line) > 0:
            updates.append([int(u) for u in line.split(",")])
            line = in_stream.readline().strip()

    return rules, updates


def get_correct_middles(rules, updates):
    middles = []
    for update_line in updates:
        if are_updates_valid(rules, update_line)[0]:
            middles.append(update_line[int(len(update_line)/2)])

    return middles


def set_and_get_correct_middles(rules, updates):
    middles = []
    retry_cnt = 0
    for update_line in updates:
        is_valid, i, j = are_updates_valid(rules, update_line)
        if is_valid:
            continue

        while not is_valid and retry_cnt < 10000:
            temp = update_line[i]
            update_line[i] = update_line[j]
            update_line[j] = temp

            is_valid, i, j = are_updates_valid(rules, update_line)
            retry_cnt += 1

        if retry_cnt == 10000:
            print(f"Exceeded retry count: {update_line}")
        middles.append(update_line[int(len(update_line) / 2)])

    return middles


def are_updates_valid(rules, update_line):
    for i in range(0, len(update_line)-1):
        update = update_line[i]
        for j in range(i+1, len(update_line)):
            if update not in rules or update_line[j] not in rules[update]:
                return False, i, j

    return True, -1, -1


rule_lines, update_lines = load_input()
rules = {}
for rule in rule_lines:
    if rule[0] not in rules:
        rules[rule[0]] = set()
    rules[rule[0]].add(rule[1])

print(f"Sum of valid middles: {sum(get_correct_middles(rules, update_lines))}")
print(f"Sum of valid middles after fixing them: {sum(set_and_get_correct_middles(rules, update_lines))}")

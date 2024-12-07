def load_input():
    with open('in07', 'r') as in_stream:
        return [(int(line.split(":")[0]), [int(o) for o in line.split(":")[1].strip().split(" ")]) for line in in_stream.readlines()]


def get_valid_equations(equations, allow_concatenation=False):
    valid = []
    for target, operands in equations:
        if is_valid_equation(target, operands, 1, operands[0], allow_concatenation):
            valid.append(target)

    return valid


def is_valid_equation(target, operands, operator_index, running_total, allow_concatenation=False):
    if operator_index == len(operands):
        return target == running_total

    if running_total > target:
        return False

    is_valid = is_valid_equation(target, operands, operator_index + 1, running_total + operands[operator_index], allow_concatenation) \
           or is_valid_equation(target, operands, operator_index + 1, running_total * operands[operator_index], allow_concatenation)

    if allow_concatenation and not is_valid:
        is_valid = is_valid_equation(target, operands, operator_index + 1, concat_int(running_total, operands[operator_index]), allow_concatenation)

    return is_valid


def concat_int(a, b):
    return int(str(a) + str(b))


equations = load_input()
valid_targets = get_valid_equations(equations)
print(f"Valid equation targets: {valid_targets}")
print(f"Which sum to {sum(valid_targets)}")

valid_targets = get_valid_equations(equations, allow_concatenation=True)
print(f"Valid equation targets with concatenation: {valid_targets}")
print(f"Which sum to {sum(valid_targets)}")

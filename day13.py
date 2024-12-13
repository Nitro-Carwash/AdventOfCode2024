import re


Button = tuple[int, int]
Target = tuple[int, int]
Machine = tuple[Button, Button, Target]

conversion_adjustment = 10000000000000


def load_input() -> list[Machine]:
    with open('in13', 'r') as in_stream:
        input_machines: list[Machine] = []
        while True:
            line = in_stream.readline().strip()
            if len(line) == 0:
                break

            tuples: list[tuple[int, int]] = []
            for regex in [r"Button A: X\+(\d+), Y\+(\d+)", r"Button B: X\+(\d+), Y\+(\d+)", r"Prize: X=(\d+), Y=(\d+)"]:
                groups = re.match(regex, line)
                tuples.append((int(groups.group(1)), int(groups.group(2))))
                line = in_stream.readline().strip()

            input_machines.append((tuples[0], tuples[1], tuples[2]))

        return input_machines


# It's Cramer's Rule!!!!!!
def solve_machine(a: Button, b: Button, target: Target, limit_presses=True):
    determinant = a[0]*b[1] - a[1]*b[0]
    if determinant == 0:
        return 0

    a_determinant = (target[0]*b[1]-target[1]*b[0])
    if a_determinant % determinant != 0:
        return 0

    b_determinant = (target[1]*a[0]-target[0]*a[1])
    if b_determinant % determinant != 0:
        return 0

    a_presses = int(a_determinant / determinant)
    b_presses = int(b_determinant / determinant)
    if limit_presses and (a_presses > 100 or b_presses > 100):
        return 0

    return 3*a_presses + b_presses


machines = load_input()
print(f"Total cost for winning all machines: {sum([solve_machine(a, b, target) for a, b, target in machines])}")
print(f"Total cost for winning all machines after adjusting for conversion error: {sum([solve_machine(a, b, (target[0] + conversion_adjustment, target[1] + conversion_adjustment), False) for a, b, target in machines])}")

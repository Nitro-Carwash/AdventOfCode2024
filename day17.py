import math
import re

class ProgramState:
    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c
        self.out = []


def load_input() -> (ProgramState, list[int]):
    with open('in17', 'r') as in_stream:
        machine = []
        for line in [l.strip() for l in in_stream.readlines() if l.strip() != ""]:
            groups = re.match(r".*: (.*)", line.strip())
            machine.append(groups.group(1))

        return ProgramState(int(machine[0]), int(machine[1]), int(machine[2])), [int(i) for i in machine[3].split(',')]



op_to_instruction = {
    0: lambda state, operand : adv(state, operand),
    1: lambda state, operand : bxl(state, operand),
    2: lambda state, operand : bst(state, operand),
    3: lambda state, operand : jnz(state, operand),
    4: lambda state, operand : bxc(state, operand),
    5: lambda state, operand : out(state, operand),
    6: lambda state, operand : bdv(state, operand),
    7: lambda state, operand : cdv(state, operand),
}


def adv(state: ProgramState, operand: int):
    state.a = int(state.a / math.pow(2, get_operand_value(state, operand)))


def bxl(state: ProgramState, operand: int):
    state.b = operand ^ state.b


def bst(state: ProgramState, operand: int):
    state.b = get_operand_value(state, operand) % 8


def jnz(state: ProgramState, operand: int):
    if state.a != 0:
        return operand


def bxc(state: ProgramState, operand: int):
    state.b = state.b ^ state.c


def out(state: ProgramState, operand: int):
    state.out.append(str(get_operand_value(state, operand) % 8))


def bdv(state: ProgramState, operand: int):
    state.b = int(state.a / math.pow(2, get_operand_value(state, operand)))


def cdv(state: ProgramState, operand: int):
    state.c = int(state.a / math.pow(2, get_operand_value(state, operand)))


def get_operand_value(state: ProgramState, operand: int):
    if operand <= 3:
        return operand
    if operand == 4:
        return state.a
    if operand == 5:
        return state.b
    if operand == 6:
        return state.c


def solve():
    program_state, program = load_input()
    pointer = 0
    it = 0
    while pointer < len(program):
        it += 1
        next_pointer_pos = op_to_instruction[program[pointer]](program_state, program[pointer + 1])
        pointer = next_pointer_pos if next_pointer_pos is not None else pointer + 2

    print(",".join(program_state.out))

solve()
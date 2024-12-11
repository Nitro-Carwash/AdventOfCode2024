def load_input():
    with open('in11', 'r') as in_stream:
        return [int(t) for t in in_stream.readline().strip().split(' ')]


def calculate_split_stones(stone: int, remaining_depth: int, memo):
    if stone in memo and remaining_depth in memo[stone]:
        return memo[stone][remaining_depth]

    if remaining_depth == 0:
        return 1
    if stone == 0:
        return calculate_split_stones(1, remaining_depth - 1, memo)

    stone_str = str(stone)
    stone_length = len(stone_str)
    if stone_length % 2 == 0:
        half_len = int(stone_length/2)
        splits = calculate_split_stones(int(stone_str[:half_len]), remaining_depth - 1, memo) \
                 + calculate_split_stones(int(stone_str[half_len:]), remaining_depth - 1, memo)
        add_to_memo(stone, remaining_depth, splits, memo)
        return splits
    else:
        splits = calculate_split_stones(stone * 2024, remaining_depth - 1, memo)
        add_to_memo(stone, remaining_depth, splits, memo)
        return splits


def add_to_memo(stone: int, remaining_depth: int, value: int, memo):
    if stone not in memo:
        memo[stone] = {}
    memo[stone][remaining_depth] = value


memo = {}
initial_stones = load_input()
split_stones = [calculate_split_stones(stone, 25, memo) for stone in initial_stones]
print(f"Total split stones after 25 blinks: {sum(split_stones)}")

split_stones = [calculate_split_stones(stone, 75, memo) for stone in initial_stones]
print(f"Total split stones after 75 blinks: {sum(split_stones)}")

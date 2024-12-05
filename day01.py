import re


def load_input():
    col1 = []
    col2 = []
    with open('in01', 'r') as in_stream:
        for line in in_stream.readlines():
            groups = re.match(r"(\d+)\s+(\d+)", line)
            col1.append(int(groups.group(1)))
            col2.append(int(groups.group(2)))

    return col1, col2


# Part 1
def calculate_total_distance(col1, col2):
    col1 = sorted(col1)
    col2 = sorted(col2)

    total_distance = 0

    for i in range(len(col1)):
        total_distance += abs(col1[i] - col2[i])

    return total_distance


# Part 2
def calculate_similarity_score(col1, col2):
    freq_dict = {}
    for v in col2:
        if v in freq_dict:
            freq_dict[v] += 1
        else:
            freq_dict[v] = 1

    total_similarity = 0
    for v in col1:
        if v in freq_dict:
            total_similarity += v * freq_dict[v]

    return total_similarity


col1, col2 = load_input()
print(f"total distance: {calculate_total_distance(col1, col2)}")
print(f"similarity score: {calculate_similarity_score(col1, col2)}")

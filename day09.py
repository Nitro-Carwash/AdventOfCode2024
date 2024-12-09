def load_input():
    with open('in09', 'r') as in_stream:
        return [int(c) for c in in_stream.readline()]


def fragmented_compression_sum(disk_map):
    total = 0
    left_pointer = 0
    right_pointer = len(disk_map) - 1 if len(disk_map) % 2 != 0 else len(disk_map) - 2
    i = 0
    while left_pointer <= right_pointer:
        # If this block is already filled, just get the checksum and move on
        if left_pointer % 2 == 0:
            file_id = int((left_pointer / 2))
            file_size = disk_map[left_pointer]
            total += calculate_block_checksum(i, file_size, file_id)
            i += file_size
            left_pointer += 1

        # If this block is empty, try to fill a bit then add it to the checksum
        else:
            if disk_map[right_pointer] == 0:
                right_pointer -= 2
            elif disk_map[left_pointer] == 0:
                left_pointer += 1
            else:
                total += int(i * (right_pointer / 2))  # file id of a filled position is pos/2
                disk_map[right_pointer] -= 1
                disk_map[left_pointer] -= 1
                i += 1

    return total


def defragmented_compression_sum(disk_map):
    total = 0
    original_disk = disk_map.copy()
    right_pointer = len(disk_map) - 1 if len(disk_map) % 2 != 0 else len(disk_map) - 2

    # Iterate from the right, trying to find a place to move each block as far left as possible.
    # Add the file to the checksum if it can be moved
    while right_pointer > 0:
        file_size = disk_map[right_pointer]
        if file_size > 0:
            left_pointer = 1

            # Try to find a place for this file
            while left_pointer < right_pointer and disk_map[left_pointer] < file_size:
                left_pointer += 2

            # If a place was found, add it to the checksum from its new location and remove it from the disk_map
            if left_pointer < right_pointer and disk_map[left_pointer] >= file_size:
                # index = sum of all blocks up to here, plus any free space here that has potentially already been used
                # in a previous move
                i = sum(original_disk[:left_pointer]) + original_disk[left_pointer] - disk_map[left_pointer]

                file_id = int((right_pointer / 2))
                total += calculate_block_checksum(i, file_size, file_id)
                disk_map[right_pointer] = 0
                # Only remove the amount of free space that was actually used
                disk_map[left_pointer] -= file_size

        right_pointer -= 2

    # Finally, accumulate all blocks that did not move
    left_pointer = 0
    i = 0
    while left_pointer < len(disk_map):
        if left_pointer % 2 == 0:
            block_size = disk_map[left_pointer]
            file_id = int((left_pointer / 2))
            total += calculate_block_checksum(i, block_size, file_id)

        # Always use the original disk's block size to move the index because we have modified the disk_map
        i += original_disk[left_pointer]
        left_pointer += 1

    return total


def calculate_block_checksum(block_start_index, file_size, file_id):
    sum_of_indices = block_start_index * file_size + int(file_size * (file_size - 1) / 2)
    return sum_of_indices * file_id



disk_map = load_input()
fragmented_compression = fragmented_compression_sum(disk_map)
print(f"Fragmented compression: {fragmented_compression}")

disk_map = load_input()
defragmented_compression = defragmented_compression_sum(disk_map)
print(f"Defragmented compression: {defragmented_compression}")


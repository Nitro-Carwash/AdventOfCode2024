# Requires PyPNG

import re
from functools import reduce
from operator import mul
import png

image_subdirectory = "day14/"

Vec2 = tuple[int, int]
Robot = tuple[Vec2, Vec2]

world_width = 101
world_height = 103
time_cutoff = 10000
world_width_half = int(world_width/2)
world_height_half = int(world_height/2)


def load_input() -> list[Robot]:
    with open('in14', 'r') as in_stream:
        robots: list[Robot] = []
        for line in in_stream.readlines():
            groups = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
            robots.append(((int(groups.group(1)), int(groups.group(2))), (int(groups.group(3)), int(groups.group(4)))))

        return robots


def calculate_safety(robots: list[Robot], seconds):
    quadrants = [0, 0, 0, 0]
    border_count = 0
    for robot in robots:
        quadrant = get_final_robot_quadrant(robot, seconds)
        if quadrant >= 0:
            quadrants[quadrant] += 1
        else:
            border_count += 1

    return reduce(mul, quadrants)


def get_final_robot_quadrant(robot: Robot, seconds: int):
    pos = robot[0]
    velocity = robot[1]
    for _ in range(seconds):
        pos = ((pos[0] + velocity[0]) % world_width, (pos[1] + velocity[1]) % world_height)

    if pos[0] == world_width_half or pos[1] == world_height_half:
        return -1

    if pos[0] < world_width_half:
        return 0 if pos[1] < world_height_half else 2
    return 1 if pos[1] < world_height_half else 3


def iterate_and_draw(robots: list[Robot]):
    world = [[0 for _ in range(world_width)] for _ in range(world_height)]
    time = 0

    while time < time_cutoff:
        positions = set()
        time += 1

        for i in range(len(robots)):
            robot = robots[i]
            pos = robot[0]
            v = robot[1]
            robot = robots[i] = (((pos[0] + v[0]) % world_width, (pos[1] + v[1]) % world_height), v)
            pos = robot[0]
            positions.add(pos)

        mark_world_with_robots(world, robots)
        draw_and_save_world(world, f"{time}")
        mark_world_with_robots(world, robots, True)


def mark_world_with_robots(world, robots: list[Robot], clear=False):
    for robot in robots:
        pos = robot[0]
        world[pos[1]][pos[0]] = 0 if clear else 255


def draw_and_save_world(world, filename):
    writer = png.Writer(width=world_width, height=world_height, bitdepth=8, greyscale=True)
    with open(f'{image_subdirectory}{filename}.png', 'wb') as f:
        writer.write(f, world)


def print_world(world):
    for row in world:
        print (".".join(row))

robots = load_input()
print(f"Total safety: {calculate_safety(robots, 100)}")
print(f"This next step will generate {time_cutoff} images in {image_subdirectory}.  Each image is about 700 bytes.")
print(f"This means that it will take up about {time_cutoff * 700} bytes on your disk (or about {time_cutoff * 700 / 1000}kb)")

confirm = input("Enter [Yy] if you want to do this, or anything else to abort.")
if confirm.lower() == 'y':
    print("Generating images....")
    iterate_and_draw(robots)
    print("Done!")
else:
    print("Cancelling part 2")


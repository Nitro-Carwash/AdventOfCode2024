import math


def load_input():
    with open('in02', 'r') as in_stream:
        return [[int(r) for r in line.split()] for line in in_stream.readlines()]


# Part 1 & 2
def count_safe_reports(reports):
    safe_total = 0
    safe_total_with_dampening = 0
    for report in reports:
        safe, failed = is_report_safe(report)
        if safe:
            safe_total += 1
            safe_total_with_dampening += 1
        else:
            report_without_middle = report[:]
            report_without_middle.pop(failed)
            if is_report_safe(report_without_middle)[0]:
                safe_total_with_dampening += 1
                continue

            report_without_right = report[:]
            report_without_right.pop(failed+1)
            if is_report_safe(report_without_right)[0]:
                safe_total_with_dampening += 1
                continue

            if failed > 0:
                report_without_left = report[:]
                report_without_left.pop(failed-1)
                if is_report_safe(report_without_left)[0]:
                    safe_total_with_dampening += 1
                    continue

    return safe_total, safe_total_with_dampening


def is_report_safe(report):
    if not is_pair_safe(report[0], report[1]):
        return False, 0

    sign = math.copysign(1, report[1] - report[0])
    for i in range(2, len(report)):
        if not is_pair_safe(report[i - 1], report[i], sign):
            return False, i - 1

    return True, -1


def is_pair_safe(a, b, sign=None):
    diff = b - a
    abs_diff = abs(diff)
    if abs_diff < 1 or abs_diff > 3:
        return False
    if sign is not None and math.copysign(1, diff) != sign:
        return False

    return True


reports = load_input()
safe_total, safe_total_with_dampening = count_safe_reports(reports)
print(f"total safe reports: {safe_total}")
print(f"total safe reports with problem dampening: {safe_total_with_dampening}")

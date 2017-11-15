"""Credits and levels computations.
"""
from itertools import accumulate, chain
from typing import Iterator, Tuple, List

from learn.models import Student, Task, Level


def total_credits_for_levels(levels: List[Level]) -> Iterator[Tuple[Level, int]]:
    needed_credits = accumulate(chain([0], levels), lambda c, l: c + l.credits)
    # last accumulated value is not used - student can't go beyond the last level
    return zip(levels, needed_credits)


def get_needed_credits(levels: List[Level], which_level: Level) -> int:
    for level, credits in total_credits_for_levels(levels):
        if level == which_level:
            return credits
    raise ValueError('Unknown level: {level}'.format(level=which_level))


def get_level(world, student):
    levels = list(world.levels.all())
    level = levels[0]
    for next_level, needed_credits in total_credits_for_levels(levels):
        if student.credits >= needed_credits:
            level = next_level
        else:
            return level
    return level


def get_level_value(world, student):
    return get_level(world, student).level


def get_active_credits(world, student):
    level = get_level(world, student)
    passive_credits = get_needed_credits(world.levels, level)
    active_credits = student.credits - passive_credits
    return active_credits


def get_credits(task: Task) -> int:
    """Number of credits for solving given task.
    """
    level = task.level.level
    credits = (level + 1) ** 2
    return credits


def get_earned_credits(student: Student, task: Task) -> int:
    """Number of credits earned for solving given task by given student.

    It is 0 if the student has already solved this task before.
    """
    solved_before = student.task_sessions.filter(task=task, solved=True).exists()
    if solved_before:
        return 0
    return get_credits(task)

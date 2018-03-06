"""Credits and levels computations.
"""
from learn.models import Student, Task


def get_level_value(world, student):
    # TODO: Unfake using mastery info.
    return 1


def get_active_credits(world, student):
    # TODO: Remove active credtis completely.
    return 0


def get_credits(task: Task) -> int:
    # TODO: Unfake using mission level.
    return 1


def get_earned_credits(student: Student, task: Task) -> int:
    """Number of credits earned for solving given task by given student.

    It is 0 if the student has already solved this task before.
    """
    solved_before = student.task_sessions.filter(task=task, solved=True).exists()
    if solved_before:
        return 0
    return get_credits(task)

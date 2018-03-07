"""Credits and levels computations.
"""
from learn.models import Student, Task


def get_level(domain, student):
    # TODO: Unfake using mastery info (number of mastered missions).
    return 1


def get_earned_credits(student: Student, task: Task) -> int:
    """Number of credits earned for solving given task by given student.

    It is 0 if the student has already solved this task before.
    """
    solved_before = student.task_sessions.filter(task=task, solved=True).exists()
    if solved_before:
        return 0
    # TODO: More credits if it was a recommended task.
    return 1

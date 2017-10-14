""" Techniques for task recommendation

Task recommender protocol: world, student -> task (or None)
"""
import random
from learn.credits import get_level_value
from learn.student_task import has_solved


def randomly_by_level(world, student):
    """Select task randomly from the current level, sometimes from lower levels.

    Only select from unsolved tasks.
    Probability of selection depends on the difference between the level of the
    student and the level of the task.

    Args:
        world: learn.world.World
        student: learn.model.Student

    Returns:
        (learn.models.Task) recommended task
    """
    student_level = get_level_value(world, student)
    tasks = [
        task for task in world.tasks
        if task.level.level <= student_level and not has_solved(student, task)]
    if not tasks:
        return None
    weighted_tasks = _exponentially_weighted_tasks(tasks, student_level)
    sum_of_weights = sum(weight for _, weight in weighted_tasks)
    number = random.randint(0, sum_of_weights - 1)
    return _roulette_wheel_selection(weighted_tasks, number)


def _exponentially_weighted_tasks(tasks, preferred_level, decay_factor=0.5):
    """Give weights to the tasks based on their levels.

    Args:
        tasks: tasks to weight
        preferred_level: tasks on this level are preferred
        decay_factor: factor of probability decay between levels

    Return:
        list of tuples (task, weight)
    """
    weighted_tasks = [
        (task, int(100 * decay_factor ** abs(task.level.level - preferred_level)))
        for task in tasks]
    return weighted_tasks


def _roulette_wheel_selection(weighted_tasks, number):
    """Select from the list based on weights and given random number

    Args:
        weighted_tasks: list of tuples with task id and weight
        number: randomly generated number between [0, sum of all weights)

    Return:
        selected task
    """
    if number < 0:
        raise ValueError("Number must be positive.")
    for task, weight in weighted_tasks:
        if number < weight:
            return task
        number -= weight
    raise ValueError("Number must be less than the sum of all weights in the list.")

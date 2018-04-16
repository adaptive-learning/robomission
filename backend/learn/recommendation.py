""" Techniques for task recommendation

Task recommender protocol: domain, chunk, student -> task (or None)
"""
from collections import namedtuple
import random
from learn.mastery import get_first_unsolved_mission, get_first_unsolved_phase


Recommendation = namedtuple('Recommendation', [
    'available',
    'mission',
    'phase',
    'task',
])


def get_recommendation(domain, student):
    mission = select_mission(domain, student)
    if not mission:
        return Recommendation(available=False, mission=None, phase=None, task=None)
    phase = select_phase(mission, student)
    task = select_task(phase, student)
    return Recommendation(
        available=True,
        mission=mission.name,
        phase=phase.name,
        task=task.name)


def select_mission(domain, student):
    return get_first_unsolved_mission(domain, student)


def select_phase(mission, student):
    return get_first_unsolved_phase(mission, student)


def select_task(ps, student):
    solved_tasks = {ts.task for ts in student.task_sessions.all() if ts.solved}
    unsolved_tasks = set(ps.tasks.all()) - solved_tasks
    return random.choice(list(unsolved_tasks))

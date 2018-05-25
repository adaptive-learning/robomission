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
    'levels',
])


def get_recommendation(domain, student):
    mission = select_mission(domain, student)
    if not mission:
        return create_unavailable_recommendation()
    phase = select_phase(mission, student)
    if not phase:
        return create_unavailable_recommendation()
    task = select_task(phase, student)
    if not task:
        return create_unavailable_recommendation()
    return Recommendation(
        available=True,
        mission=mission.name,
        phase=phase.name,
        task=task.name,
        levels=task.levels)


def select_mission(domain, student):
    return get_first_unsolved_mission(domain, student)


def select_phase(mission, student):
    return get_first_unsolved_phase(mission, student)


def select_task(ps, student):
    solved_tasks = {ts.task for ts in student.task_sessions.all() if ts.solved}
    unsolved_tasks = set(ps.tasks.all()) - solved_tasks
    return random.choice(list(unsolved_tasks)) if unsolved_tasks else None


def create_unavailable_recommendation():
    return Recommendation(available=False, mission=None, phase=None, task=None, levels=None)

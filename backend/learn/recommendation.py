""" Techniques for task recommendation

Task recommender protocol: domain, chunk, student -> task (or None)
"""
from collections import namedtuple
import random


Recommendation = namedtuple('Recommendation', [
    'available',
    'mission',
    'phase',
    'task',
])


def get_recommendation(domain, student):
    # TODO: decompose: select mission -> phase -> task
    #if task is None:
    #    return Recommendation(available=False, mission=None, phase=None, task=None)
    #return Recommendation(
    #    available=True,
    #    mission=task.chunk.mission.name,
    #    phase=task.chunk.step.name,
    #    task=task.name)
    raise NotImplementedError

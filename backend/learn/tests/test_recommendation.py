import pytest

from learn.models import Task, Level
from learn.recommendation import _exponentially_weighted_tasks


def level(lvl):
    return Level(level=lvl, name='a-level')

def task_at_level(lvl):
    task = Task(name='a-task', level=level(lvl))
    return task


def test_exponentially_weighted_tasks__empty_list():
    weighted_tasks = _exponentially_weighted_tasks([], preferred_level=5)
    assert weighted_tasks == []


def test_exponentially_weighted_tasks__prefer_preferred_level():
    tasks = [task_at_level(3), task_at_level(4), task_at_level(5)]
    weighted_tasks = _exponentially_weighted_tasks(tasks, preferred_level=4)
    weights = [weight for _task, weight in weighted_tasks]
    assert weights[1] > weights[0]
    assert weights[1] > weights[2]


def test_exponentially_weighted_tasks__decay_factor():
    tasks = [task_at_level(3), task_at_level(4), task_at_level(5)]
    weighted_tasks = _exponentially_weighted_tasks(
        tasks, preferred_level=5, decay_factor=0.9, max_weight=1000)
    weight3, weight4, weight5 = [weight for _task, weight in weighted_tasks]
    assert weight5 == 1000
    assert weight4 == 900
    assert weight3 == 810


def test_exponentially_weighted_tasks__always_positive_weight():
    tasks = [task_at_level(3)]
    weighted_tasks = _exponentially_weighted_tasks(
        tasks, preferred_level=10, decay_factor=0.1)
    weight = weighted_tasks[0][1]
    assert weight > 0

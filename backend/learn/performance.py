"""Compressing program sessions into a discrete performance measure.
"""
from learn.models import TaskSession, DomainParam


DEFAULT_GOOD_TIME = 5 * 60  # 5 mins


def compute_performance(domain, task_session):
    if not task_session.solved:
        return TaskSession.UNSOLVED
    if task_session.time_spent <= get_excellent_time(domain, task_session.task):
        return TaskSession.EXCELLENT
    if task_session.time_spent <= get_good_time(domain, task_session.task):
        return TaskSession.GOOD
    return TaskSession.POOR


def get_excellent_time(domain, task):
    good_time = get_good_time(domain, task)
    excellent_time = int(good_time / 2)
    return excellent_time


def get_good_time(domain, task):
    try:
        return domain.params.get(name='good_time', chunk=task).value
    except DomainParam.DoesNotExist:
        return DEFAULT_GOOD_TIME

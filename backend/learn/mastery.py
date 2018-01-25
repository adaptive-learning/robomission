"""Mastery learning.
"""
from learn.models import Chunk

SKILL_FOR_MASTERY = 0.95

#PERFORMANCE_VALUES_MAP = {
#    TaskSession.UNSOLVED: 0,
#    TaskSession.POOR: 0.1,
#    TaskSession.GOOD: 0.5,
#    TaskSession.EXCELLENT: 1,
#}
#
#
#def performance_to_value(performance, n_tasks):
#    base_value = PERFORMANCE_VALUES_MAP[performance]
#    min_value = 1 / n_tasks
#    value = max(base_value, min_value)
#    return value
#
#
#def get_skill(student, chunk):
#    performances = student.task_sessions.filter(task__chunk=chunk).all()
#    n_tasks = chunk.tasks.count()
#    performance_values = [performance_to_value(p, n_tasks) for p in performances]
#    skill = min(1, sum(performance_values))
#    return skill


def has_mastered(student, chunk):
    skill = student.get_skill(chunk)
    return skill >= SKILL_FOR_MASTERY


def get_first_unmastered_chunk(student, chunks):
    # Chunks are ordered in DB layer.
    for chunk in chunks:
        if not has_mastered(student, chunk):
            return chunk
    # The student could have mastered all chunks.
    return None

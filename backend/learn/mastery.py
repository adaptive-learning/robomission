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
    subchunks_mastered = (has_mastered(student, c) for c in chunk.subchunks.all())
    all_subchunks_mastered = all(subchunks_mastered)
    skill = student.get_skill(chunk)
    return all_subchunks_mastered and skill >= SKILL_FOR_MASTERY


def get_first_unsolved_mission(domain, student):
    # TODO: has mastered mission - if all phases are solved ??
    # Missions are ordered in DB layer.
    for mission in domain.missions.all():
        if not has_mastered(student, mission.chunk):
            return mission
    # The student could have mastered all missions.
    return None


def get_first_unsolved_phase(mission, student):
    for phase in mission.phases:
        if not has_mastered(student, phase):
            return phase
    # The student could have mastered all phases of the given mission.
    return None

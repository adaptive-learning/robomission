"""Mastery learning.
"""
from statistics import mean
from learn.models import TaskSession, Skill

SKILL_FOR_MASTERY = 0.95

PERFORMANCE_VALUES_MAP = {
    TaskSession.UNSOLVED: 0,
    TaskSession.POOR: 0.1,
    TaskSession.GOOD: 0.5,
    TaskSession.EXCELLENT: 1,
}


def performance_to_value(performance, n_tasks):
    base_value = PERFORMANCE_VALUES_MAP[performance]
    min_value = 1 / n_tasks
    value = max(base_value, min_value)
    return value


def update_skills(student, task, performance):
    for phase in task.chunks.all():
        update_base_skill(student, phase, performance)
        # TODO: If the chunk graph structure become any DAG, then update all
        # parent chunks recursively.
        update_parent_skill(student, phase.parents.first())


def update_base_skill(student, chunk, performance):
    skill, _created = Skill.objects.get_or_create(student=student, chunk=chunk)
    delta = performance_to_value(performance, chunk.n_tasks)
    skill.value = min(1, skill.value + delta)
    skill.save()


def update_parent_skill(student, chunk):
    skill, _created = Skill.objects.get_or_create(student=student, chunk=chunk)
    skill.value = mean(student.get_skill(c) for c in chunk.subchunks.all())
    skill.save()


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

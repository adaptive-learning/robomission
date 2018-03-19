"""Mastery learning.
"""
from collections import namedtuple
from statistics import mean
from learn.models import TaskSession, Skill

SKILL_FOR_MASTERY = 0.95

PERFORMANCE_VALUES_MAP = {
    TaskSession.UNSOLVED: 0,
    TaskSession.POOR: 0.1,
    TaskSession.GOOD: 0.5,
    TaskSession.EXCELLENT: 1,
}


Progress = namedtuple('Progress', [
    'chunk',
    'skill',
])


def performance_to_value(performance, n_tasks):
    base_value = PERFORMANCE_VALUES_MAP[performance]
    min_value = 1 / n_tasks
    value = max(base_value, min_value)
    return value


def get_skills(domain, student):
    skills = {chunk.name: 0 for chunk in domain.chunks.all()}
    for skill in student.skills.all():
        skills[skill.chunk.name] = skill.value
    return skills


def update_skills(student, task, performance):
    progress = []
    for phase in task.chunks.all():
        skill = update_base_skill(student, phase, performance)
        progress.append(Progress(phase.name, skill.value))
        # TODO: If the chunk graph structure become any DAG, then update all
        # parent chunks recursively.
        parent_chunk = phase.parents.first()
        skill = update_parent_skill(student, parent_chunk)
        progress.append(Progress(parent_chunk.name, skill.value))
    return progress


def update_base_skill(student, chunk, performance):
    skill, _created = Skill.objects.get_or_create(student=student, chunk=chunk)
    delta = performance_to_value(performance, chunk.n_tasks)
    skill.value = min(1, skill.value + delta)
    skill.save()
    return skill


def update_parent_skill(student, chunk):
    skill, _created = Skill.objects.get_or_create(student=student, chunk=chunk)
    skill.value = mean(student.get_skill(c) for c in chunk.subchunks.all())
    skill.save()
    return skill


def has_mastered(student, chunk):
    subchunks_mastered = (has_mastered(student, c) for c in chunk.subchunks.all())
    all_subchunks_mastered = all(subchunks_mastered)
    skill = student.get_skill(chunk)
    return all_subchunks_mastered and skill >= SKILL_FOR_MASTERY


def get_current_mission_phase(domain, student):
    mission = get_first_unsolved_mission(domain, student)
    phase = get_first_unsolved_phase(mission, student)
    return mission, phase


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


def get_level(domain, student):
    """Level is number of solved missions + 1 (in order to start on level 1).
    """
    n_solved_missions = sum(
        int(has_mastered(student, mission.chunk))
        for mission in domain.missions.all())
    return n_solved_missions + 1

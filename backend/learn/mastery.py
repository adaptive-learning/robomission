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
    # TODO(once doman.chunks exists): Generalized to domain.chunks.all()
    # instead of domain.problemsets.all().
    skills = {ps.name: 0 for ps in domain.problemsets.all()}
    for skill in student.skills.all():
        skills[skill.chunk.name] = skill.value
    return skills


def update_skills(student, task, performance):
    progress = []
    phase = task.problemset
    if phase:
        skill = update_base_skill(student, phase, performance)
        progress.append(Progress(phase.name, skill.value))
    mission = task.mission
    if mission:
        skill = update_parent_skill(student, mission)
        progress.append(Progress(mission.name, skill.value))
    return progress


def update_base_skill(student, ps, performance):
    skill, _created = Skill.objects.get_or_create(student=student, chunk=ps)
    delta = performance_to_value(performance, ps.n_tasks)
    skill.value = min(1, skill.value + delta)
    skill.save()
    return skill


def update_parent_skill(student, ps):
    skill, _created = Skill.objects.get_or_create(student=student, chunk=ps)
    skill.value = mean(student.get_skill(part) for part in ps.parts.all())
    skill.save()
    return skill


def has_mastered(student, ps):
    parts_mastered = (has_mastered(student, part) for part in ps.parts.all())
    all_parts_mastered = all(parts_mastered)
    skill = student.get_skill(ps)
    return all_parts_mastered and skill >= SKILL_FOR_MASTERY


def get_current_mission_phase(domain, student):
    mission = get_first_unsolved_mission(domain, student)
    phase = get_first_unsolved_phase(mission, student)
    return mission, phase


def get_first_unsolved_mission(domain, student):
    # TODO: has mastered mission - if all phases are solved ??
    # Missions are ordered in DB layer.
    for mission in domain.missions.all():
        if not has_mastered(student, mission):
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
        int(has_mastered(student, mission))
        for mission in domain.missions.all())
    return n_solved_missions + 1

from collections import namedtuple
from learn.mastery import get_level, get_skills
from learn.mastery import get_current_mission_phase
from learn.student_task import has_attempted, has_solved, get_time
from learn.recommendation import get_recommendation


PracticeOverview = namedtuple('PracticeOverview', [
    'level',
    'mission',
    'phase',
    'credits',
    'tasks',
    'skills',
    'recommendation',
])


StudentTask = namedtuple('StudentTask', [
    'name',
    'attempted',
    'solved',
    'time',
])


StudentSkill = namedtuple('StudentSkill', [
    'name',
    'value',
])


def get_tasks(domain, student):
    student_tasks = [
        StudentTask(
            name=task.name,
            attempted=has_attempted(student, task),
            solved=has_solved(student, task),
            time=get_time(student, task))
        for task in domain.tasks.all()]
    return student_tasks


def get_skill_list(domain, student):
    skill_dict = get_skills(domain, student)
    skill_list = [
        StudentSkill(name=key, value=value)
        for key, value in skill_dict.items()]
    return skill_list


def get_practice_overview(domain, student):
    # TODO: Remove redundancy of get_current_mission_phase vs get_recommendation.
    mission, phase = get_current_mission_phase(domain, student)
    overview = PracticeOverview(
        level=get_level(domain, student),
        mission=mission.name if mission else None,
        phase=phase.name if phase else None,
        credits=student.credits,
        tasks=get_tasks(domain, student),
        skills=get_skill_list(domain, student),
        recommendation=get_recommendation(domain, student),
    )
    return overview

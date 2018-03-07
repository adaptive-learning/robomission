from collections import namedtuple
from learn.mastery import get_level
from learn.student_task import has_attempted, has_solved, get_time
from learn.recommendation import get_recommendation


PracticeOverview = namedtuple('PracticeOverview', [
    'level',
    'credits',
    'tasks',
    'recommendation',
])


StudentTask = namedtuple('StudentTask', [
    'name',
    'attempted',
    'solved',
    'time',
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


def get_practice_overview(domain, student):
    overview = PracticeOverview(
        level=get_level(domain, student),
        credits=student.credits,
        tasks=get_tasks(domain, student),
        recommendation=get_recommendation(domain, student),
    )
    return overview

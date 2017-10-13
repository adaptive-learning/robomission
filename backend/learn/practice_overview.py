from collections import namedtuple
from learn.credits import get_active_credits, get_level_value
from learn.student_task import has_attempted, has_solved, get_time
from learn import recommendation


PracticeOverview = namedtuple('PracticeOverview', [
    'level',
    'credits',
    'active_credits',
    'instructions',
    'tasks',
    'recommendation',
])


StudentInstruction = namedtuple('StudentInstruction', [
    'name',
    'seen',
])


StudentTask = namedtuple('StudentTask', [
    'name',
    'attempted',
    'solved',
    'time',
])


Recommendation = namedtuple('Recommendation', [
    'available',
    'task',
])


def get_recommendation(world, student):
    task = recommendation.randomly_by_level(world, student)
    return Recommendation(available=task is not None, task=task.name)


def get_instructions_overview(world, student):
    instructions_overview = [
        StudentInstruction(
            name=instruction.name,
            seen=instruction in student.seen_instructions.all())
            # It's important for the student.seen_instrustions to be
            # prefetched, otherwise a SQL query will be spawned for each
            # instruction.
        for instruction in world.instructions]
    return instructions_overview


def get_tasks(world, student):
    student_tasks = [
        StudentTask(
            name=task.name,
            attempted=has_attempted(student, task),
            solved=has_solved(student, task),
            time=get_time(student, task))
        for task in world.tasks]
    return student_tasks


def get_practice_overview(world, student):
    overview = PracticeOverview(
        level=get_level_value(world, student),
        credits=student.credits,
        active_credits=get_active_credits(world, student),
        instructions=get_instructions_overview(world, student),
        tasks=get_tasks(world, student),
        recommendation=get_recommendation(world, student),
    )
    return overview

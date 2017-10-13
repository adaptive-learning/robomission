from collections import namedtuple
#from flocs.student import get_active_credits, get_instructions, get_tasks, get_level
#from flocs.recommendation import random_by_level

PracticeOverview = namedtuple('PracticeOverview', [
    'level',
    'credits',
    'active_credits',
    'instructions',
    'tasks',
    'recommendation',
])


# TODO: move it to separate module
Recommendation = namedtuple('Recommendation', [
    'available',
    'task',
])


StudentInstruction = namedtuple('StudentInstruction', [
    'name',
    'seen',
])


StudentTask = namedtuple('StudentTask', [
    'name',
    'solved',
    'time',
])


def get_recommendation(world, student):
    # TODO: compute real recommendation
    return Recommendation(available=True, task='one-step-forward')


def get_instructions_overview(world, student):
    instructions_overview = [
        StudentInstruction(
            name=instruction.name,
            seen=instruction in student.seen_instructions.all(),
            # It's important for the student.seen_instrustions to be
            # prefetched, otherwise a SQL query will be spawned for each
            # instruction.
        )
        for instruction in world.instructions]
    return instructions_overview


def get_tasks(world, student):
    # TODO: implement
    return []


def get_active_credits(world, student):
    # TODO: implement
    return 0


def get_practice_overview(world, student):
    overview = PracticeOverview(
        level=0,
        credits=student.credits,
        active_credits=get_active_credits(world, student),
        instructions=get_instructions_overview(world, student),
        tasks=get_tasks(world, student),
        recommendation=get_recommendation(world, student),
    )
    return overview

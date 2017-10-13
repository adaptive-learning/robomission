from collections import namedtuple
from learn.credits import get_active_credits, get_level_value


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
    'attempted',
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


def has_attempted(student, task):
    return any(ts.task == task for ts in student.task_sessions.all())


def has_solved(student, task):
    return any(ts.solved for ts in student.task_sessions.all() if ts.task == task)


def get_time(student, task):
    """Return the best time from solved sessions, or last time if not solved.
    """
    task_sessions = [ts for ts in student.task_sessions.all() if ts.task == task]
    if not task_sessions:
        return None
    solved_sessions = [ts for ts in task_sessions if ts.solved]
    if solved_sessions:
        times = [ts.time_spent for ts in solved_sessions]
        return min(times)
    last_task_session = max(task_sessions, key=lambda ts: ts.end)
    return last_task_session.time_spent


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

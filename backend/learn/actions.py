""" Actions represent events and interactions in the domain we want to model.
"""
from django.utils import timezone
from learn.credits import get_earned_credits
from learn.models import Action, TaskSession, ProgramSnapshot
from learn.student_task import get_current_task_session
from learn.mastery import update_skills
from learn.performance import compute_performance


def start_task(domain, student, task_name):
    task = domain.tasks.get(name=task_name)
    task_session = get_current_task_session(student, task)

    if task_session is not None:
        # task has been already started, so this is a duplicate actions and
        # we don't wan't to save it again
        duplicate_action = Action(
            name=Action.START_TASK,
            student=student,
            task=task,
            data={'task_session_id': task_session.pk})
        return duplicate_action

    task_session = TaskSession(
        student=student,
        task=task)
    task_session.save()
    action = Action(
        name=Action.START_TASK,
        student=student,
        task=task,
        data={'task_session_id': task_session.pk})
    action.save()
    return action


def edit_program(task_session, program):
    if task_session.solved:
        return

    student = task_session.student
    task = task_session.task

    task_session.end = timezone.now()
    snapshot = ProgramSnapshot(
        task_session_id=task_session.pk,
        granularity=ProgramSnapshot.EDIT,
        program=program)
    action = Action(
        name=Action.EDIT_PROGRAM,
        student=student,
        task=task,
        data={
            'program': program,
            'task_session_id': task_session.pk})

    # TODO: factor db updates out
    task_session.save()
    snapshot.save()
    action.save()

    return action


def run_program(domain, task_session, program, correct):
    if task_session.solved:
        return
    student = task_session.student
    task = task_session.task
    task_session.end = timezone.now()
    snapshot = ProgramSnapshot(
        task_session_id=task_session.pk,
        granularity=ProgramSnapshot.EXECUTION,
        program=program,
        correct=correct)
    action = Action(
        name=Action.RUN_PROGRAM,
        student=student,
        task=task,
        data={
            'task_session_id': task_session.pk,
            'program': program,
            'correct': correct})
    # TODO: factor db updates out
    progress = []
    if correct:
        progress = solve_task(domain, task_session)
    task_session.save()
    snapshot.save()
    action.save()
    return progress
    #return action


def solve_task(domain, task_session):
    if task_session.solved:
        return
    student = task_session.student
    task = task_session.task
    task_session.end = timezone.now()
    task_session.solved = True
    task_session.performance = compute_performance(domain, task_session)
    progress = update_skills(student, task, task_session.performance)
    student.credits += get_earned_credits(student, task)
    student.save()
    task_session.save()
    return progress

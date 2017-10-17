""" Actions represent events and interactions in the world we want to model.
"""
from django.utils import timezone
from learn.models import Action, TaskSession, ProgramSnapshot


def start_task(world, student, task_name):
    task = world.tasks.get(name=task_name)
    TaskSession.objects.create(
        student=student,
        task=task)
    Action.objects.create(
        name=Action.START_TASK,
        student=student,
        task=task)


def watch_instruction(world, student, instruction_name):
    instruction = world.instructions.get(name=instruction_name)
    student.seen_instructions.add(instruction)
    Action.objects.create(
        name=Action.WATCH_INSTRUCTION,
        student=student,
        data={'instruction': instruction_name})


def edit_program(world, task_session, program):
    if task_session.solved:
        return

    student = task_session.student
    task = world.tasks.get(name=task_session.task.name)

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

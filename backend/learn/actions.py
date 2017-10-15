""" Actions represent events and interactions in the world we want to model.
"""
from learn.models import Action, TaskSession


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

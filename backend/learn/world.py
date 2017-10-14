from collections import namedtuple
from learn.models import Block, Toolbox, Level, Task, Instruction


World = namedtuple('World', [
    'blocks',
    'toolboxes',
    'levels',
    'tasks',
    'instructions',
])


def get_world(include=('blocks', 'toolboxes', 'levels', 'tasks', 'instructions')):
    """Create a world of static entities.

    Each attribute is a queryset with specified related entities prefetching.
    """
    world = World(
        blocks=(
            Block.objects.all()
            if 'blocks' in include
            else None),
        toolboxes=(
            Toolbox.objects.prefetch_related('blocks').all()
            if 'toolboxes' in include
            else None),
        levels=(
            Level.objects.prefetch_related('tasks').all()
            if 'levels' in include
            else None),
        tasks=(
            Task.objects.select_related('level').all()
            if 'tasks' in include
            else None),
        instructions=(
            Instruction.objects.all()
            if 'instructions' in include
            else None))
    return world

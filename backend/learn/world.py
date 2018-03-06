from collections import namedtuple
from learn.models import Block, Toolbox, Task, Instruction


World = namedtuple('World', [
    'blocks',
    'toolboxes',
    'tasks',
    'instructions',
])


def get_world(include=('blocks', 'toolboxes', 'tasks', 'instructions')):
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
        tasks=(
            Task.objects.all()
            if 'tasks' in include
            else None),
        instructions=(
            Instruction.objects.all()
            if 'instructions' in include
            else None))
    return world

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
    world = World(
        blocks=Block.objects.all() if  'blocks' in include else None,
        toolboxes=Toolbox.objects.all() if 'toolboxes' in include else None,
        levels=Level.objects.all() if 'levels' in include else None,
        tasks=Task.objects.all() if 'tasks' in include else None,
        instructions=Instruction.objects.all() if 'instructions' in include else None)
    return world

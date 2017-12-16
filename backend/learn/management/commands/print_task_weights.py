from django.core.management.base import BaseCommand
from learn.world import get_world
from learn.recommendation import _exponentially_weighted_tasks


class Command(BaseCommand):
    help = "Print weights of all tasks in DB for given student level"

    def add_arguments(self, parser):
        parser.add_argument(
            '--level',
            type=int,
            default=1,
        )

    def handle(self, *args, **options):
        level = options['level']
        world = get_world()
        tasks = [task for task in world.tasks if task.level.level <= level]
        weighted_tasks = _exponentially_weighted_tasks(tasks, preferred_level=level)
        for task, weight in sorted(weighted_tasks, key=lambda tw: (-tw[1], tw[0].name)):
            self.stdout.write('{weight} {task} (L{level})'.format(
                weight=weight, task=task, level=task.level.level))

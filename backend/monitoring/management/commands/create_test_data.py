from django.core.management.base import BaseCommand
from django.conf import settings
from learn.models import Student, Task, TaskSession, ProgramSnapshot



class Command(BaseCommand):
    help = 'Create test data (events) and store them to DB.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--n_events',
            help='How many events to generate.'
        )


    def handle(self, *args, **options):
        n_events = int(options['n_events'])
        student = Student.objects.create()
        task = Task.objects.first()
        ts = TaskSession.objects.create(student=student, task=task)
        ProgramSnapshot.objects.bulk_create([
            ProgramSnapshot(task_session=ts, program='frl')
            for i_event in range(n_events)
        ])

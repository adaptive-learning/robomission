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
            ProgramSnapshot(
                task_session=ts,
                granularity='execution' if i_event % 10 == 0 else 'edit',
                correct=(i_event % 20 == 0) if i_event % 10 == 0 else None,
                program='frl',
                time_from_start=15,  # inconsistent, but ok for testing
            )
            for i_event in range(n_events)
        ])

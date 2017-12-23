from django.core.management.base import BaseCommand
from monitoring.metrics import MetricsComputer


class Command(BaseCommand):
    help = "Compute all metrics since last date they were computed."

    def handle(self, *args, **options):
        metrics_computer = MetricsComputer()
        self.stdout.write(
            'Computing metrics from {first_date} to {last_date} ...'.format(
                first_date=metrics_computer.first_date,
                last_date=metrics_computer.last_date))
        metrics_computer.compute_and_save()
        self.stdout.write('Metrics computed and stored to DB.')

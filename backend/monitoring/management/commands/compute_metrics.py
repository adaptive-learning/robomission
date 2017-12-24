from datetime import datetime
from django.core.management.base import BaseCommand
from monitoring.metrics import MetricsComputer


class Command(BaseCommand):
    help = "Compute all metrics since last date they were computed."

    def add_arguments(self, parser):
        parser.add_argument(
            '--from',
            help='Date from which to recompute all metrics (YYYY-MM-DD)'
        )

    def handle(self, *args, **options):
        first_date = None
        if options['from']:
            first_date = datetime.strptime(options['from'], '%Y-%m-%d').date()
        metrics_computer = MetricsComputer(first_date=first_date)
        self.stdout.write(
            'Computing metrics from {first_date} to {last_date} ...'.format(
                first_date=metrics_computer.first_date,
                last_date=metrics_computer.last_date))
        for metric in metrics_computer.generate_and_save():
            self.stdout.write('-- {metric}'.format(metric=metric))
        self.stdout.write('Done. Computed metrics were stored to DB.')

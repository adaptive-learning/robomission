from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from monitoring.metrics import make_metrics_generator


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Compute all metrics since last date they were computed."

    def add_arguments(self, parser):
        parser.add_argument(
            '--from',
            help='Date from which to recompute all metrics (YYYY-MM-DD)'
        )

    def handle(self, *args, **options):
        logger.info('Management command called: compute_metrics')
        first_date = None
        if options['from']:
            first_date = datetime.strptime(options['from'], '%Y-%m-%d').date()
        generate_metrics, dates = make_metrics_generator(first_date=first_date)
        if not dates:
            self.stderr.write('Empty date range. No metrics generated.')
            return
        self.stdout.write(
            'Computing metrics from {first_date} to {last_date} ...'.format(
                first_date=dates[0],
                last_date=dates[-1]))
        for metric in generate_metrics():
            self.stdout.write('-- {metric}'.format(metric=metric))
        self.stdout.write('Done. Computed metrics were stored to DB.')

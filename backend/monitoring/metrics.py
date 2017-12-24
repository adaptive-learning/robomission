"""Definition of metrics we care about.
"""
from collections import defaultdict
from datetime import timedelta, time, datetime
from django.db.models import Count
from django.db.models.functions import Trunc
from django.utils import timezone
from monitoring.models import Metric
from learn.models import Action, TaskSession


def get_last_measured_date():
    last_metric = Metric.objects.last()
    return last_metric.time if last_metric else None


def get_first_unmeasured_date():
    last_measured_date = get_last_measured_date()
    if last_measured_date:
        return last_measured_date + timedelta(days=1)
    else:
        return Action.objects.first().time.date()


def get_yesterday():
    return timezone.now().date() - timedelta(days=1)


def to_timezone_aware(date, last_second=False):
    time_part = time.max if last_second else time.min
    aware_datetime = datetime.combine(date, time_part, tzinfo=timezone.utc)
    return aware_datetime


class MetricsComputer:
    def __init__(self, first_date=None):
        self.first_date = first_date or get_first_unmeasured_date()
        self.last_date = get_yesterday()

    def generate_and_save(self):
        metrics = self.compute()
        for metric in metrics:
            metric.save()
            yield metric

    def compute(self):
        # If the first_date was set by user, it's necessary to delete
        # previously computed metrics before they are replaced by the new
        # values.
        Metric.objects.filter(time__gte=self.first_date).delete()
        # Daily Active Students = students who have solved at least 1 task
        time_range = (
            to_timezone_aware(self.first_date),
            to_timezone_aware(self.last_date, last_second=True))
        dates_with_values = (
            TaskSession.objects
            .annotate(date=Trunc('end', 'day'))
            .filter(date__range=time_range, solved=True)
            .values('date')
            .annotate(count=Count('student_id', distinct=True)))
        # We use defaultdict to return 0 for dates missing in the aggregation.
        date_to_value = defaultdict(
            int,
            ((group['date'].date(), group['count']) for group in dates_with_values))
        n_days = (self.last_date - self.first_date).days + 1
        dates = [self.first_date + timedelta(days=d) for d in range(n_days)]
        for date in dates:
            yield Metric(name='active-students', time=date, value=date_to_value[date])

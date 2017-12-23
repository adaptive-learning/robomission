"""Definition of metrics we care about.
"""
from datetime import timedelta
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


class MetricsComputer:
    def __init__(self):
        self.first_date = get_first_unmeasured_date()
        self.last_date = get_yesterday()

    def compute_and_save(self):
        metrics = self.compute()
        for metric in metrics:
            print(metric)
            #metric.save()

    def compute(self):
        # Daily Active Users = students who have solved at least 1 task
        dates_with_DAU = (
            TaskSession.objects
            .annotate(date=Trunc('end', 'day'))
            .filter(date__range=(self.first_date, self.last_date), solved=True)
            .values('date')
            .annotate(count=Count('student_id', distinct=True)))
        for date_with_dau in dates_with_DAU:
            date = date_with_dau['date'].date()
            count = date_with_dau['count']
            yield Metric(name='1DAU', time=date, value=count)

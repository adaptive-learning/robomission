"""Definition of metrics we care about.
"""
from collections import defaultdict
from datetime import timedelta, time, datetime
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


def dates_range(first_date, last_date):
    n_days = (last_date - first_date).days + 1
    dates = [first_date + timedelta(days=d) for d in range(n_days)]
    return dates


def group_by_date(task_sessions):
    groups = defaultdict(list)
    for ts in task_sessions:
        groups[ts.date].append(ts)
    return groups


def generate_active_students_metric(task_sessions, dates):
    """Yield active-students metric for each date in dates.

    Active student = has solve at least 1 task (in given day).
    """
    solved_task_sessions = [ts for ts in task_sessions if ts.solved]
    groups = group_by_date(solved_task_sessions)
    for date in dates:
        n_active_students = len({ts.student_id for ts in groups[date]})
        yield Metric(name='active-students', time=date, value=n_active_students)


def generate_solved_tasks_metric(task_sessions, dates):
    """Yield solved-tasks metric for each date in dates.
    """
    solved_task_sessions = [ts for ts in task_sessions if ts.solved]
    groups = group_by_date(solved_task_sessions)
    for date in dates:
        n_solved_tasks = len(groups[date])
        yield Metric(name='solved-tasks', time=date, value=n_solved_tasks)


def generate_solving_hours_metric(task_sessions, dates):
    """Yield solving-time metric for each date in dates.
    """
    solved_task_sessions = [ts for ts in task_sessions if ts.solved]
    groups = group_by_date(solved_task_sessions)
    hour = 3600
    for date in dates:
        total_solving_hours = sum(ts.time_spent for ts in groups[date]) / hour
        yield Metric(name='solving-hours', time=date, value=total_solving_hours)


def generate_metrics(dates):
    time_range = (to_timezone_aware(dates[0]), to_timezone_aware(dates[-1], last_second=True))
    task_sessions = list(TaskSession.objects.filter(end__date__range=time_range))
    yield from generate_active_students_metric(task_sessions, dates)
    yield from generate_solved_tasks_metric(task_sessions, dates)
    yield from generate_solving_hours_metric(task_sessions, dates)


def make_metrics_generator(first_date=None):
    """Return metrics generator and dates for which will be metrics computed.
    """
    first_date = first_date or get_first_unmeasured_date()
    last_date = get_yesterday()
    dates = dates_range(first_date, last_date)

    def generate_and_save_metrics():
        # If the first_date was set manually, it's necessary to delete
        # previously computed metrics before they are replaced by the new ones.
        Metric.objects.filter(time__gte=first_date).delete()
        for metric in generate_metrics(dates):
            metric.save()
            yield metric

    return generate_and_save_metrics, dates

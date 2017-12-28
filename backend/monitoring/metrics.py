"""Definition of metrics we care about.
"""
from collections import defaultdict
from statistics import mean, median
from datetime import timedelta, time, datetime
from django.utils import timezone
from monitoring.models import Metric
from learn.models import Action, Task, TaskSession


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
    naive_datetime = datetime.combine(date, time_part)
    aware_datetime = timezone.make_aware(naive_datetime, timezone=timezone.utc)
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


def group_by_task(task_sessions):
    groups = defaultdict(list)
    for ts in task_sessions:
        groups[ts.task_id].append(ts)
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


def generate_solved_count_metric(task_sessions, dates):
    """Yield solved-count metric for each date in dates.
    """
    solved_task_sessions = [ts for ts in task_sessions if ts.solved]
    groups = group_by_date(solved_task_sessions)
    for date in dates:
        n_solved_tasks = len(groups[date])
        yield Metric(name='solved-count', time=date, value=n_solved_tasks)


def generate_solved_count_for_task_metric(task_sessions, date, tasks):
    """Yield solved-count metric for each task and given date.
    """
    recent_solved_task_sessions = [
        ts for ts in task_sessions
        if ts.solved and ts.date > date - timedelta(days=30)]
    groups = group_by_task(recent_solved_task_sessions)
    for task in tasks:
        solved_count = len(groups[task.id])
        group_name = 'task.' + task.name
        yield Metric(
            name='solved-count', group=group_name, time=date,
            value=solved_count)


def compute_success_ratio(task_sessions):
    return mean(ts.solved for ts in task_sessions) if task_sessions else 0


def generate_success_ratio_metric(task_sessions, dates):
    """Yield success-ratio metric for each date in dates.
    """
    groups = group_by_date(task_sessions)
    for date in dates:
        success_ratio = compute_success_ratio(groups[date])
        yield Metric(name='success-ratio', time=date, value=success_ratio)


def generate_success_ratio_for_task_metric(task_sessions, date, tasks):
    """Yield success ratio metric for each task and given date.
    """
    recent_task_sessions = [
        ts for ts in task_sessions
        if ts.date > date - timedelta(days=30)]
    groups = group_by_task(recent_task_sessions)
    for task in tasks:
        success_ratio = compute_success_ratio(groups[task.id])
        group_name = 'task.' + task.name
        yield Metric(
            name='success-ratio', group=group_name, time=date,
            value=success_ratio)


def generate_solving_hours_metric(task_sessions, dates):
    """Yield solving-time metric for each date in dates.
    """
    solved_task_sessions = [ts for ts in task_sessions if ts.solved]
    groups = group_by_date(solved_task_sessions)
    hour = 3600
    for date in dates:
        total_solving_hours = sum(ts.time_spent for ts in groups[date]) / hour
        yield Metric(name='solving-hours', time=date, value=total_solving_hours)


def generate_median_time_for_task_metric(task_sessions, date, tasks):
    """Yield median-time metric for each task and given date.
    """
    recent_solved_task_sessions = [
        ts for ts in task_sessions
        if ts.solved and ts.date > date - timedelta(days=30)]
    groups = group_by_task(recent_solved_task_sessions)
    for task in tasks:
        times = [ts.time_spent for ts in groups[task.id]]
        median_time = median(times) if times else 0
        group_name = 'task.' + task.name
        yield Metric(name='median-time', group=group_name, time=date, value=median_time)


def generate_metrics(dates):
    # Select all task sessions which might be possibly needed.
    time_range = (
        to_timezone_aware(min(dates[0], dates[-1] - timedelta(days=30))),
        to_timezone_aware(dates[-1], last_second=True))
    # NOTE: If you add a new metric, make sure to prefetch requried data (such
    # as task_session.snapshots or task_session.task) to avoid excess SQL
    # queries). Currently, only a separate lists of TaskSessions and Tasks are
    # enought for all computation.
    # TODO: test that no SQL queries are generated in metrics generators
    task_sessions = list(TaskSession.objects.filter(end__date__range=time_range))
    # global metrics
    yield from generate_active_students_metric(task_sessions, dates)
    yield from generate_solved_count_metric(task_sessions, dates)
    yield from generate_success_ratio_metric(task_sessions, dates)
    yield from generate_solving_hours_metric(task_sessions, dates)
    # task-specific metrics
    tasks = list(Task.objects.all())
    yield from generate_solved_count_for_task_metric(task_sessions, dates[-1], tasks)
    yield from generate_success_ratio_for_task_metric(task_sessions, dates[-1], tasks)
    yield from generate_median_time_for_task_metric(task_sessions, dates[-1], tasks)


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
        # Delete recent group-specific metrics - it's not necessary to store
        # them for every day.
        group_metrics = Metric.objects.filter(group__isnull=False)
        recent_group_metrics = group_metrics.filter(time__gt=last_date-timedelta(days=10))
        recent_group_metrics.delete()
        new_metrics = []
        for metric in generate_metrics(dates):
            new_metrics.append(metric)
            yield metric
        # All generated metris are stored to DB in a single SQL query.
        Metric.objects.bulk_create(new_metrics)

    return generate_and_save_metrics, dates

import pytest

from learn.models import Task, Domain, DomainParam
from learn.models import Student, TaskSession, ProgramSnapshot
from learn.performance import compute_performance
from learn.utils.time import ms


@pytest.mark.django_db
def test_compute_performance__unsolved():
    task = Task.objects.create(name='t1', setting='{}', solution='')
    domain = Domain.objects.create()
    domain.tasks.set([task])
    domain.params.create(name='good_time', task=task, value=2*60)
    student = Student.objects.create()
    ts = TaskSession.objects.create(
        student=student, task=task, solved=False, start=ms('0:00'), end=ms('1:00'))
    assert compute_performance(domain, ts) == TaskSession.UNSOLVED


@pytest.mark.django_db
def test_compute_performance__poor():
    task = Task.objects.create(name='t1', setting='{}', solution='')
    domain = Domain.objects.create()
    domain.tasks.set([task])
    domain.params.create(name='good_time', task=task, value=2*60)
    student = Student.objects.create()
    ts = TaskSession.objects.create(
        student=student, task=task, solved=True, start=ms('0:00'), end=ms('3:00'))
    assert compute_performance(domain, ts) == TaskSession.POOR


@pytest.mark.django_db
def test_compute_performance__good():
    task = Task.objects.create(name='t1', setting='{}', solution='')
    domain = Domain.objects.create()
    domain.tasks.set([task])
    domain.params.create(name='good_time', task=task, value=2*60)
    student = Student.objects.create()
    ts = TaskSession.objects.create(
        student=student, task=task, solved=True, start=ms('0:00'), end=ms('1:30'))
    assert compute_performance(domain, ts) == TaskSession.GOOD


@pytest.mark.django_db
def test_compute_performance__excellent():
    task = Task.objects.create(name='t1', setting='{}', solution='')
    domain = Domain.objects.create()
    domain.tasks.set([task])
    domain.params.create(name='good_time', task=task, value=2*60)
    student = Student.objects.create()
    ts = TaskSession.objects.create(
        student=student, task=task, solved=True, start=ms('0:00'), end=ms('0:30'))
    assert compute_performance(domain, ts) == TaskSession.EXCELLENT

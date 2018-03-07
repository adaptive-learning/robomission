from unittest import mock
import pytest
from django.test import TestCase
from django.utils import timezone
from learn.models import Task, Chunk, Mission, Domain
from learn.models import Student, TaskSession, Skill
from learn.actions import solve_task
from learn.utils.time import ms


def create_domain():
    # TODO: Allow to set domain briefly, sth. like:
    #       create_domain('m1(p1(t1, t2, t3), p2(t4, t5))').
    t1 = Task.objects.create(name='t1', setting='{}', solution='')
    c1 = Chunk.objects.create(name='c1')
    p1 = Chunk.objects.create(name='p1', order=1)
    p2 = Chunk.objects.create(name='p2', order=2)
    m1 = Mission.objects.create(name='m1', chunk=c1)
    c1.subchunks.set([p1, p2])
    p1.tasks.set([t1])
    domain = Domain.objects.create()
    domain.missions.set([m1])
    domain.chunks.set([c1, p1, p2])
    domain.tasks.set([t1])
    return domain

class SolveTaskTestCase(TestCase):
    def test_set_solved(self):
        domain = create_domain()
        student = Student.objects.create()
        task = domain.tasks.get(name='t1')
        ts = TaskSession.objects.create(student=student, task=task)
        solve_task(domain, ts)
        ts.refresh_from_db()
        assert ts.solved

    def test_set_performance(self):
        domain = create_domain()
        student = Student.objects.create()
        task = domain.tasks.get(name='t1')
        ts = TaskSession.objects.create(student=student, task=task)
        solve_task(domain, ts)
        ts.refresh_from_db()
        assert ts.performance != TaskSession.UNSOLVED

    def test_ignore_duplicates(self):
        domain = create_domain()
        student = Student.objects.create()
        task = domain.tasks.get(name='t1')
        ts = TaskSession.objects.create(student=student, task=task)
        with mock.patch('django.utils.timezone.now', return_value=ms('1:00')):
            solve_task(domain, ts)
        same_ts = TaskSession.objects.get(pk=ts.pk)
        with mock.patch('django.utils.timezone.now', return_value=ms('2:00')):
            with self.assertNumQueries(0):
                solve_task(domain, same_ts)
        assert ts.end == same_ts.end

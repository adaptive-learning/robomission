from datetime import date
from django.test import TestCase
from django.utils import timezone
from learn.models import Block, Task, Chunk, Student, Skill, TaskSession
from learn.models import ProgramSnapshot


class BlockTestCase(TestCase):
    def test_blocks_exists(self):
        assert Block.objects.exists()

    def test_blocks_are_ordered(self):
        first_retrieved_blocks = list(Block.objects.all())[:3]
        first_expected_blocks = [
            Block.objects.get(name='fly'),
            Block.objects.get(name='shoot'),
            Block.objects.get(name='repeat')]
        assert first_retrieved_blocks == first_expected_blocks

    def test_str_returns_name(self):
        carrot_block = Block(name='carrot', order=4)
        assert str(carrot_block) == 'carrot'


class ChunkTestCase(TestCase):
    def test_chunks_are_ordered(self):
        chunk1 = Chunk.objects.create(name='c1', order=2)
        chunk2 = Chunk.objects.create(name='c2', order=1)
        assert list(Chunk.objects.all()) == [chunk2, chunk1]


class StudentTestCase(TestCase):
    def test_get_skill__existing(self):
        chunk = Chunk.objects.create(name='c1')
        student = Student.objects.create()
        Skill.objects.create(student=student, chunk=chunk, value=0.25)
        assert student.get_skill(chunk) == 0.25

    def test_get_skill__nonexisting(self):
        chunk = Chunk.objects.create(name='c1')
        student = Student.objects.create()
        assert student.get_skill(chunk) == 0

    def test_str(self):
        student = Student.objects.create(id=10)
        assert str(student) == 's10'


class TaskSessionTestCase(TestCase):
    def test_date(self):
        task = Task(id=1, name='t1', setting='{}', solution='')
        student = Student.objects.create()
        ts = TaskSession.objects.create(
            student=student, task=task,
            start=timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc),
            end=timezone.datetime(2017, 1, 1, 8, 2, 0, tzinfo=timezone.utc))
        assert ts.date == date(2017, 1, 1)

    def test_time_spent(self):
        task = Task(id=1, name='t1', setting='{}', solution='')
        student = Student.objects.create()
        ts = TaskSession.objects.create(
            student=student, task=task,
            start=timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc),
            end=timezone.datetime(2017, 1, 1, 8, 2, 5, tzinfo=timezone.utc))
        assert ts.time_spent == 125

    def test_str(self):
        task = Task(id=5, name='carrot', setting='{}', solution='')
        student = Student.objects.create(id=10)
        ts = TaskSession.objects.create(id=11, student=student, task=task)
        assert str(ts) == '[11] s10-carrot'

    def test_performance_is_ordered(self):
        assert TaskSession.UNSOLVED < TaskSession.POOR
        assert TaskSession.POOR < TaskSession.GOOD
        assert TaskSession.GOOD < TaskSession.EXCELLENT


class ProgramSnapshotTestCase(TestCase):
    def test_str(self):
        snapshot = ProgramSnapshot(id=5, program='ffr')
        assert str(snapshot) == '[5] ffr'

    def test_order_first(self):
        ts = _create_task_session()
        snapshot = ProgramSnapshot.objects.create(task_session=ts)
        assert snapshot.order == 1

    def test_order_first_for_given_granularity(self):
        ts = _create_task_session()
        edit_snapshot = ProgramSnapshot.objects.create(
            task_session=ts, granularity=ProgramSnapshot.EDIT)
        execution_snapshot = ProgramSnapshot.objects.create(
            task_session=ts, granularity=ProgramSnapshot.EXECUTION)
        assert edit_snapshot.order == 1
        assert execution_snapshot.order == 1

    def test_order_by_time(self):
        ts = _create_task_session()
        snapshot1 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc))
        snapshot2 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 10, tzinfo=timezone.utc))
        assert snapshot1.order == 1
        assert snapshot2.order == 2

    def test_order_by_time_within_granularity(self):
        ts = _create_task_session()
        edit_snapshot1 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc),
            granularity=ProgramSnapshot.EDIT)
        execution_snapshot1 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 10, tzinfo=timezone.utc),
            granularity=ProgramSnapshot.EXECUTION)
        edit_snapshot2 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 20, tzinfo=timezone.utc),
            granularity=ProgramSnapshot.EDIT)
        assert edit_snapshot1.order == 1
        assert execution_snapshot1.order == 1
        assert edit_snapshot2.order == 2

    def test_time_from_start(self):
        ts = _create_task_session_at(timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc))
        snapshot = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 10, tzinfo=timezone.utc))
        assert snapshot.time_from_start == 10


def _create_task_session():
    task = Task.objects.create(name='carrot', setting='{}', solution='')
    student = Student.objects.create()
    ts = TaskSession.objects.create(student=student, task=task)
    return ts


def _create_task_session_at(time):
    task = Task.objects.create(name='carrot', setting='{}', solution='')
    student = Student.objects.create()
    ts = TaskSession.objects.create(student=student, task=task, start=time)
    return ts

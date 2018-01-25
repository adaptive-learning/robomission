import pytest

from learn.models import Student, Task, Chunk, TaskSession, Skill
from learn.mastery import get_first_unmastered_chunk
from learn.mastery import has_mastered, get_first_unmastered_chunk


@pytest.fixture
def initial_student():
    student = Student()
    return student


@pytest.fixture
def task1():
    task = Task(id=1, name='t1', setting='{}', solution='')
    return task


@pytest.fixture
def chunk_with_1_task(task1):
    chunk = Chunk(id=1)
    chunk.tasks = [task1]
    return chunk


# Django DB is always needed for many-to-many relations (chunks.tasks)
@pytest.mark.django_db
def test_has_mastered__initially_not(initial_student, chunk_with_1_task):
    assert not has_mastered(initial_student, chunk_with_1_task)


# django db is always needed for many-to-many relations (student.skills)
# todo: find a way how to test the following without using db.
@pytest.mark.django_db
def test_has_mastered__when_skill_is_1():
    chunk = Chunk.objects.create(name='c1')
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=chunk, value=1.0)
    assert has_mastered(student, chunk)


@pytest.mark.django_db
def test_has_mastered__not_when_skill_is_low():
    chunk = Chunk.objects.create(name='c1')
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=chunk, value=0.5)
    assert not has_mastered(student, chunk)


@pytest.mark.django_db
def test_get_first_unmastered_chunk__single():
    chunk = Chunk.objects.create(name='c1')
    student = Student.objects.create()
    assert get_first_unmastered_chunk(student) == chunk


@pytest.mark.django_db
def test_get_first_unmastered_chunk__all_unmastered():
    chunk1 = Chunk.objects.create(name='c1')
    Chunk.objects.create(name='c2')
    student = Student.objects.create()
    assert get_first_unmastered_chunk(student) == chunk1


@pytest.mark.django_db
def test_get_first_unmastered_chunk__first_mastered():
    chunk1 = Chunk.objects.create(name='c1')
    chunk2 = Chunk.objects.create(name='c2')
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=chunk1, value=1)
    assert get_first_unmastered_chunk(student) == chunk2


#@pytest.mark.django_db
#def test_has_mastered__excellent_performance():
#    task1 = Task.objects.create(id=1, name='t1', setting='{}', solution='')
#    task2 = Task.objects.create(id=2, name='t2', setting='{}', solution='')
#    chunk = Chunk.objects.create(id=1, name='c1')
#    chunk.tasks.set([task1, task2])
#    # Id=1 already taken by the student "initial" created in a DB migration.
#    student = Student.objects.create(id=2)
#    ts = TaskSession.objects.create(
#        student=student, task=task1, performance=TaskSession.EXCELLENT)
#    assert has_mastered(student, chunk)

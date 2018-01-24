import pytest

from learn.models import Student, Task, Chunk
from learn.mastery import get_first_unmastered_chunk
from learn.mastery import is_mastered


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


# Django DB is always needed form many-to-many relations (chunks.tasks)
@pytest.mark.django_db
def test_is_mastered__initially_not(chunk_with_1_task, initial_student):
    assert is_mastered(chunk_with_1_task, initial_student) == False

import pytest

from learn.models import Task, Student, Toolbox, TaskSession
from learn.credits import get_credits, get_earned_credits


@pytest.fixture
def toolbox():
    return Toolbox(name="some toolbox")


@pytest.fixture
def task():
    return Task(name="some task", setting="", solution="")


@pytest.fixture
def student():
    return Student(user=None)


@pytest.mark.django_db
@pytest.fixture
def solved_task_for_student():
    toolbox = Toolbox.objects.create(name="some toolbox")
    task = Task.objects.create(name="some task", setting="", solution="")
    student = Student.objects.create(user=None)
    TaskSession.objects.create(student=student, task=task, solved=True)
    return student, task


def test_get_credits_for_task(task):
    credits = get_credits(task)
    assert credits > 0


def test_get_earner_credits_first_time(student, task):
    credits = get_earned_credits(student, task)
    assert credits > 0


@pytest.mark.django_db
def test_get_earner_credits_already_solved(solved_task_for_student):
    student, task = solved_task_for_student
    credits = get_earned_credits(student, task)
    expected_credits = 0
    assert expected_credits == credits

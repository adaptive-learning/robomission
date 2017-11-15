import pytest

from learn.models import Task, Level, Student, Toolbox, TaskSession
from learn.credits import get_credits, get_earned_credits, \
    total_credits_for_levels


@pytest.fixture
def toolbox():
    return Toolbox(name="some toolbox")


@pytest.fixture
def level(toolbox):
    return Level(level=5, name="some level", toolbox=toolbox, credits=20)


@pytest.fixture
def task(level):
    return Task(name="some task", level=level, setting="", solution="")


@pytest.fixture
def student():
    return Student(user=None)


@pytest.mark.django_db
@pytest.fixture
def solved_task_for_student():
    toolbox = Toolbox.objects.create(name="some toolbox")

    level = Level.objects.create(level=5, name="some level", toolbox=toolbox,
                                 credits=20)

    task = Task.objects.create(name="some task", level=level, setting="",
                               solution="")

    student = Student.objects.create(user=None)

    TaskSession.objects.create(student=student, task=task, solved=True)

    return student, task


@pytest.fixture
def levels():
    return [
        Level(level=1, name="some level 1", toolbox=None, credits=10),
        Level(level=2, name="some level 2", toolbox=None, credits=20),
        Level(level=3, name="some level 3", toolbox=None, credits=30)
    ]


def test_get_credits_for_task(task):
    credits = get_credits(task)
    expected_credits = (5 + 1) ** 2
    assert expected_credits == credits


def test_get_earner_credits_first_time(student, task):
    credits = get_earned_credits(student, task)
    expected_credits = (5 + 1) ** 2
    assert expected_credits == credits


@pytest.mark.django_db
def test_get_earner_credits_already_solved(solved_task_for_student):
    student, task = solved_task_for_student
    credits = get_earned_credits(student, task)
    expected_credits = 0
    assert expected_credits == credits


def test_total_credits_for_levels_empty():
    level_credits = total_credits_for_levels([])
    expected_level_credits = []
    assert expected_level_credits == list(level_credits)


def test_total_credits_for_levels(levels):
    level_credits = total_credits_for_levels(levels)
    expected_level_credits = [(levels[0], 0), (levels[1], 10), (levels[2], 30)]
    assert expected_level_credits == list(level_credits)

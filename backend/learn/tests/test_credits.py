import pytest

from learn.models import Task, Student, TaskSession
from learn.credits import get_earned_credits


@pytest.mark.django_db
def test_get_earner_credits_first_time():
    student = Student.objects.create()
    task = Task.objects.create()
    credits = get_earned_credits(student, task)
    assert credits > 0


@pytest.mark.django_db
def test_get_earner_credits_already_solved():
    task = Task.objects.create()
    student = Student.objects.create()
    TaskSession.objects.create(student=student, task=task, solved=True)
    credits = get_earned_credits(student, task)
    assert credits == 0

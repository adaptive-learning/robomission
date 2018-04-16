import pytest
from learn.models import Task, ProblemSet, Domain
from learn.models import Student, TaskSession, Skill
from learn.recommendation import get_recommendation, select_task


def create_domain():
    # TODO: Allow to set domain briefly, sth. like:
    #       create_domain('m1(p1(t1, t2, t3), p2(t4, t5))').
    m1 = ProblemSet.objects.create(name='m1', section='1')
    m2 = ProblemSet.objects.create(name='m2', section='2')
    p1 = m1.add_part(name='p1')
    p2 = m1.add_part(name='p2')
    t1 = p1.add_task(name='t1')
    t2 = p2.add_task(name='t2')
    t3 = p2.add_task(name='t3')
    domain = Domain.objects.create()
    domain.problemsets.set([m1, m2, p1, p2])
    domain.tasks.set([t1, t2, t3])
    return domain


@pytest.mark.django_db
def test_recommendation_available():
    domain = create_domain()
    student = Student.objects.create()
    recommendation = get_recommendation(domain, student)
    assert recommendation.available
    assert recommendation.mission is not None
    assert recommendation.phase is not None
    assert recommendation.task is not None


@pytest.mark.django_db
def test_recommend_first_mission_and_phase_for_new_student():
    domain = create_domain()
    student = Student.objects.create()
    recommendation = get_recommendation(domain, student)
    assert recommendation.mission == 'm1'
    assert recommendation.phase == 'p1'
    assert recommendation.task == 't1'


@pytest.mark.django_db
def test_dont_recommend_solved_phase():
    domain = create_domain()
    student = Student.objects.create()
    p1 = domain.problemsets.get(name='p1')
    Skill.objects.create(student=student, chunk=p1, value=1)
    recommendation = get_recommendation(domain, student)
    assert recommendation.mission == 'm1'
    assert recommendation.phase == 'p2'
    assert recommendation.task in {'t2', 't3'}


@pytest.mark.django_db
def test_dont_recommend_solved_task():
    ps = ProblemSet.objects.create()
    t1 = ps.add_task(name='t1')
    t2 = ps.add_task(name='t2')
    student = Student.objects.create()
    TaskSession.objects.create(student=student, task=t1, solved=True)
    task = select_task(ps, student)
    assert task == t2

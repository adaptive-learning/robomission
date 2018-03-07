import pytest
from learn.models import Task, Chunk, Mission, Domain
from learn.models import Student, TaskSession, Skill
from learn.recommendation import get_recommendation, select_task


def create_domain():
    # TODO: Allow to set domain briefly, sth. like:
    #       create_domain('m1(p1(t1, t2, t3), p2(t4, t5))').
    t1 = Task.objects.create(name='t1', setting='{}', solution='')
    t2 = Task.objects.create(name='t2', setting='{}', solution='')
    t3 = Task.objects.create(name='t3', setting='{}', solution='')
    c1 = Chunk.objects.create(name='c1')
    c2 = Chunk.objects.create(name='c2')
    p1 = Chunk.objects.create(name='p1', order=1)
    p2 = Chunk.objects.create(name='p2', order=2)
    m1 = Mission.objects.create(name='m1', chunk=c1)
    m2 = Mission.objects.create(name='m2', chunk=c2)
    c1.subchunks.set([p1, p2])
    p1.tasks.set([t1])
    p2.tasks.set([t2, t3])
    domain = Domain.objects.create()
    domain.missions.set([m1, m2])
    domain.chunks.set([c1, c2, p1, p2])
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
    phase1 = domain.chunks.get(name='p1')
    Skill.objects.create(student=student, chunk=phase1, value=1)
    recommendation = get_recommendation(domain, student)
    assert recommendation.mission == 'm1'
    assert recommendation.phase == 'p2'
    assert recommendation.task in {'t2', 't3'}


@pytest.mark.django_db
def test_dont_recommend_solved_task():
    t1 = Task.objects.create(name='t1', setting='{}', solution='')
    t2 = Task.objects.create(name='t2', setting='{}', solution='')
    phase = Chunk.objects.create(name='p1')
    phase.tasks.set([t1, t2])
    student = Student.objects.create()
    TaskSession.objects.create(student=student, task=t1, solved=True)
    task = select_task(phase, student)
    assert task == t2

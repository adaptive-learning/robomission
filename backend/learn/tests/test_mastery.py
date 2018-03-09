import pytest

from learn.models import Task, Chunk, Mission, Domain
from learn.models import Student, TaskSession, Skill
from learn.mastery import has_mastered, get_level
from learn.mastery import get_first_unsolved_mission
from learn.mastery import get_first_unsolved_phase


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
def test_has_mastered__mastered_subchunks():
    chunk1 = Chunk.objects.create(name='c1')
    chunk2 = Chunk.objects.create(name='c2')
    chunk3 = Chunk.objects.create(name='c3')
    chunk1.subchunks.set([chunk2, chunk3])
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=chunk1, value=1)
    Skill.objects.create(student=student, chunk=chunk2, value=1)
    Skill.objects.create(student=student, chunk=chunk3, value=1)
    assert has_mastered(student, chunk1)


@pytest.mark.django_db
def test_has_mastered__not_when_skill_is_low():
    chunk = Chunk.objects.create(name='c1')
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=chunk, value=0.5)
    assert not has_mastered(student, chunk)


@pytest.mark.django_db
def test_has_mastered__not_unmastered_subchunk():
    chunk1 = Chunk.objects.create(name='c1')
    chunk2 = Chunk.objects.create(name='c2')
    chunk3 = Chunk.objects.create(name='c3')
    chunk1.subchunks.set([chunk2, chunk3])
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=chunk1, value=1)
    Skill.objects.create(student=student, chunk=chunk2, value=1)
    # The 3rd skill is implicitly 0.
    assert not has_mastered(student, chunk1)


@pytest.mark.django_db
def test_get_first_unsolved_mission__single():
    # TODO: Shorter domain description.
    chunk = Chunk.objects.create(name='c1')
    mission = Mission.objects.create(name='m1', chunk=chunk)
    domain = Domain.objects.create()
    domain.missions.set([mission])
    domain.chunks.set([chunk])
    student = Student.objects.create()
    assert get_first_unsolved_mission(domain, student) == mission


@pytest.mark.django_db
def test_get_first_unsolved_mission__all_unsolved():
    chunk1 = Chunk.objects.create(name='c1')
    chunk2 = Chunk.objects.create(name='c2')
    mission1 = Mission.objects.create(name='m1', chunk=chunk1)
    mission2 = Mission.objects.create(name='m2', chunk=chunk2)
    domain = Domain.objects.create()
    domain.missions.set([mission1, mission2])
    domain.chunks.set([chunk1, chunk2])
    student = Student.objects.create()
    assert get_first_unsolved_mission(domain, student) == mission1


@pytest.mark.django_db
def test_get_first_unsolved_mission__first_solved():
    chunk1 = Chunk.objects.create(name='c1')
    chunk2 = Chunk.objects.create(name='c2')
    mission1 = Mission.objects.create(name='m1', chunk=chunk1)
    mission2 = Mission.objects.create(name='m2', chunk=chunk2)
    domain = Domain.objects.create()
    domain.missions.set([mission1, mission2])
    domain.chunks.set([chunk1, chunk2])
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=chunk1, value=1)
    assert get_first_unsolved_mission(domain, student) == mission2


@pytest.mark.django_db
def test_get_first_unsolved_phase__all_unsolved():
    chunk1 = Chunk.objects.create(name='c1')
    chunk2 = Chunk.objects.create(name='c2', order=1)
    chunk3 = Chunk.objects.create(name='c3', order=2)
    chunk1.subchunks.set([chunk2, chunk3])
    mission = Mission.objects.create(name='m1', chunk=chunk1)
    student = Student.objects.create()
    assert get_first_unsolved_phase(mission, student) == chunk2


@pytest.mark.django_db
def test_get_first_unsolved_phase__first_solved():
    chunk1 = Chunk.objects.create(name='c1')
    chunk2 = Chunk.objects.create(name='c2', order=1)
    chunk3 = Chunk.objects.create(name='c3', order=2)
    chunk1.subchunks.set([chunk2, chunk3])
    mission = Mission.objects.create(name='m1', chunk=chunk1)
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=chunk2, value=1)
    assert get_first_unsolved_phase(mission, student) == chunk3


@pytest.mark.django_db
def test_get_level_for_new_student():
    chunk = Chunk.objects.create(name='c1')
    mission = Mission.objects.create(name='m1', chunk=chunk)
    domain = Domain.objects.create()
    domain.missions.set([mission])
    domain.chunks.set([chunk])
    student = Student.objects.create()
    assert get_level(domain, student) == 1


@pytest.mark.django_db
def test_level_equals_number_of_solved_missions():
    c1 = Chunk.objects.create(name='c1')
    c2 = Chunk.objects.create(name='c2')
    c3 = Chunk.objects.create(name='c3')
    m1 = Mission.objects.create(name='m1', chunk=c1)
    m2 = Mission.objects.create(name='m2', chunk=c2)
    m3 = Mission.objects.create(name='m3', chunk=c3)
    domain = Domain.objects.create()
    domain.missions.set([m1, m2, m3])
    domain.chunks.set([c1, c2, c3])
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=c1, value=1)
    Skill.objects.create(student=student, chunk=c3, value=1)
    assert get_level(domain, student) == 3

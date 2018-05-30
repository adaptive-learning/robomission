import pytest

from learn.models import Task, ProblemSet, Domain
from learn.models import Student, TaskSession, Skill
from learn.mastery import has_mastered, get_level
from learn.mastery import get_first_unsolved_mission
from learn.mastery import get_first_unsolved_phase
from learn.mastery import get_current_mission_phase


# Django DB is always needed for many-to-many relations (chunks.tasks)
@pytest.mark.django_db
def test_has_mastered__initially_not():
    ps = ProblemSet.objects.create()
    ps.add_task()
    student = Student.objects.create()
    assert not has_mastered(student, ps)


# django db is always needed for many-to-many relations (student.skills)
# todo: find a way how to test the following without using db.
@pytest.mark.django_db
def test_has_mastered__when_skill_is_1():
    ps = ProblemSet.objects.create()
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=ps, value=1.0)
    assert has_mastered(student, ps)


@pytest.mark.django_db
def test_has_mastered__mastered_parts():
    m1 = ProblemSet.objects.create()
    p1 = m1.add_part()
    p2 = m1.add_part()
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=m1, value=1)
    Skill.objects.create(student=student, chunk=p1, value=1)
    Skill.objects.create(student=student, chunk=p2, value=1)
    assert has_mastered(student, m1)


@pytest.mark.django_db
def test_has_mastered__not_when_skill_is_low():
    ps = ProblemSet.objects.create()
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=ps, value=0.5)
    assert not has_mastered(student, ps)


@pytest.mark.django_db
def test_has_mastered__not_unmastered_subchunk():
    m1 = ProblemSet.objects.create()
    p1 = m1.add_part()
    p2 = m1.add_part()
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=m1, value=1)
    Skill.objects.create(student=student, chunk=p1, value=1)
    Skill.objects.create(student=student, chunk=p2, value=0)
    assert not has_mastered(student, m1)


@pytest.mark.django_db
def test_get_first_unsolved_mission__single():
    mission = ProblemSet.objects.create()
    domain = Domain.objects.create()
    domain.problemsets.set([mission])
    student = Student.objects.create()
    assert get_first_unsolved_mission(domain, student) == mission


@pytest.mark.django_db
def test_get_first_unsolved_mission__all_unsolved():
    mission1 = ProblemSet.objects.create(section='1')
    mission2 = ProblemSet.objects.create(section='2')
    domain = Domain.objects.create()
    domain.problemsets.set([mission1, mission2])
    student = Student.objects.create()
    assert get_first_unsolved_mission(domain, student) == mission1


@pytest.mark.django_db
def test_get_first_unsolved_mission__first_solved():
    mission1 = ProblemSet.objects.create(section='1')
    mission2 = ProblemSet.objects.create(section='2')
    domain = Domain.objects.create()
    domain.problemsets.set([mission1, mission2])
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=mission1, value=1)
    assert get_first_unsolved_mission(domain, student) == mission2


@pytest.mark.django_db
def test_get_first_unsolved_phase__all_unsolved():
    m1 = ProblemSet.objects.create()
    p1 = m1.add_part()
    m1.add_part()
    student = Student.objects.create()
    assert get_first_unsolved_phase(m1, student) == p1


@pytest.mark.django_db
def test_get_first_unsolved_phase__first_solved():
    m1 = ProblemSet.objects.create()
    p1 = m1.add_part()
    p2 = m1.add_part()
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=p1, value=1)
    assert get_first_unsolved_phase(m1, student) == p2


@pytest.mark.django_db
def test_get_first_unsolved_phase__all_solved():
    m1 = ProblemSet.objects.create()
    p1 = m1.add_part()
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=p1, value=1)
    Skill.objects.create(student=student, chunk=m1, value=1)
    assert get_first_unsolved_phase(m1, student) == None


@pytest.mark.django_db
def test_get_mission_phase__all_solved():
    domain = Domain.objects.create()
    m1 = ProblemSet.objects.create()
    p1 = m1.add_part()
    domain.problemsets.set([m1, p1])
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=p1, value=1)
    Skill.objects.create(student=student, chunk=m1, value=1)
    assert get_current_mission_phase(domain, student) == (None, None)


@pytest.mark.django_db
def test_get_level_for_new_student():
    mission = ProblemSet.objects.create()
    domain = Domain.objects.create()
    domain.problemsets.set([mission])
    student = Student.objects.create()
    assert get_first_unsolved_mission(domain, student) == mission
    assert get_level(domain, student) == 1


@pytest.mark.django_db
def test_level_is_number_of_solved_missions_plus_1():
    m1 = ProblemSet.objects.create()
    m2 = ProblemSet.objects.create()
    m3 = ProblemSet.objects.create()
    domain = Domain.objects.create()
    domain.problemsets.set([m1, m2, m3])
    student = Student.objects.create()
    Skill.objects.create(student=student, chunk=m1, value=1)
    Skill.objects.create(student=student, chunk=m3, value=1)
    assert get_level(domain, student) == 3

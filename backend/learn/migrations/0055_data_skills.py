"""Compute and store skills for the tasks solved in the past.
"""
from collections import Counter
from itertools import groupby
from django.db import migrations
from django.db.models import Count


def compute_skills(apps, schema_editor):
    """Compute and store skills for the tasks solved in the past.

    To avoid too many queries, we don't process a task session one by one
    computing its perforamnce and updating skills, but rather overestimating
    by a simple approximation: for each solved task we add 0.5 to the
    corresponding skill (or 1 if the phase contains only single task).
    """
    TaskSession = apps.get_model('learn', 'TaskSession')
    ProblemSet = apps.get_model('learn', 'ProblemSet')
    Skill = apps.get_model('learn', 'Skill')

    # Remove the skills stored in the meantime to avoid double counting.
    Skill.objects.all().delete()

    # Precompute number of tasks in each phase.
    ps_with_n_tasks = ProblemSet.objects.annotate(_n_tasks=Count('tasks'))
    n_tasks = {ps: ps._n_tasks for ps in ps_with_n_tasks}

    # Prefetch all solved task sessions with related data needed later.
    task_sessions = (
        TaskSession.objects
        .select_related('task__problemset__parent')
        .select_related('student')
        .filter(solved=True))

    # Count number of solved tasks for student-PS pairs.
    solved_tasks_counts = Counter(
        (ts.student, ts.task.problemset.parent, ts.task.problemset)
        for ts in task_sessions)
    # If at least 2 tasks were solved (or the phase has only 1 task),
    # we set the skill to 1.
    phase_skills = {
        (student, mission, phase): Skill(
            student=student,
            chunk=phase,
            value=1 if count > 1 or n_tasks[phase] == 1 else 0.5)
        for (student, mission, phase), count in solved_tasks_counts.items()}
    Skill.objects.bulk_create(phase_skills.values())

    # Add skills for missions - as averages of their phases skills.
    mission_phase_skills = [
        (student, mission, skill.value)
        for (student, mission, phase), skill in phase_skills.items()]
    key = lambda student_mission: (student_mission[0].pk, student_mission[1].pk)
    sorted_mission_phase_skills = sorted(mission_phase_skills, key=key)
    n_phases = 3
    mission_skills = []
    for key, group in groupby(sorted_mission_phase_skills, key=key):
        group = list(group)
        student, mission, _ = group[0]
        skill_value = sum(skill[2] for skill in group) / n_phases
        mission_skills.append(
            Skill(student=student, chunk=mission, value=skill_value))
    Skill.objects.bulk_create(mission_skills)


def remove_skills(apps, schema_editor):
    Skill = apps.get_model('learn', 'Skill')
    db_alias = schema_editor.connection.alias
    Skill.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0054_domain_instructions'),
    ]

    operations = [
        migrations.RunPython(compute_skills, reverse_code=remove_skills),
    ]

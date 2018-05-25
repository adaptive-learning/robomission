"""Compute and store skills for the tasks solved in the past.
"""
from collections import Counter
from django.db import migrations


def compute_skills(apps, schema_editor):
    TaskSession = apps.get_model('learn', 'TaskSession')
    Skill = apps.get_model('learn', 'Skill')

    # Remove the skills stored in the meantime to avoid double counting.
    Skill.objects.all().delete()

    # To avoid too many queries, we don't process a task session one by one
    # computing its perforamnce and updating skills, but rather overestimating
    # by a simple approximation: if the student has solved any task from given
    # phase, the phase is solved (the corresponding skill is 1).

    task_sessions = TaskSession.objects.select_related('task__problemset').all()

    # Dict is used to remove duplicates (Set cannot be used, because primary
    # keys would be used to compare the skills, which are not set yet.)
    phase_skills = set({
        (ts.student.pk, ts.task.pk):
            Skill(student=ts.student, chunk=ts.task.problemset, value=1)
        for ts in task_sessions}.values())

    # Add skills for missions.
    solved_phases_counts = Counter(
        (skill.student.pk, skill.chunk.problemset.parent_mission.pk)
        for skill in phase_skills)
    mission_skills = {
        Skill(student=student_pk, chunk=mission_pk, value=count/3)
        for (student_pk, mission_pk), count in solved_phases_counts.items()}

    skills = phase_skills | mission_skills
    Skill.objects.bulk_create(skills)


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0054_domain_instructions'),
    ]

    operations = [
        migrations.RunPython(compute_skills),
    ]

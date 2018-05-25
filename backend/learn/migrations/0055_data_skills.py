"""Compute and store skills for the tasks solved in the past.
"""
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

    task_sessions = TaskSessions.objects.select_related('task__problemset').all()

    # Dict is used to remove duplicates (Set cannot be used, because primary
    # keys would be used to compare the skills, which are not set yet.)
    phase_skills = list({
        (ts.student.pk, ts.task.pk):
            Skill(student=ts.student, chunk=ts.task.problemset, value=1)
        for ts in task_sessions}.values())

    # TODO:Add skills for missions.
    # ... count unique by (student.pk, skill.chunk.problemset.parent_mission.pk)
    # mission_skills = ...

    Skill.objects.bulk_create(skills)


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0054_domain_instructions'),
    ]

    operations = [
        migrations.RunPython(compute_skills),
    ]

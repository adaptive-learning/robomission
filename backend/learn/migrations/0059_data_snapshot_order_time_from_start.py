from django.db import migrations


def compute_order_and_time_from_start(apps, schema_editor):
    """Add order and time from start to all past program snapshots.
    """
    ProgramSnapshot = apps.get_model('learn', 'ProgramSnapshot')
    snapshots = ProgramSnapshot.objects.prefetch_related('task_session').all()
    # Django doesn't support simple iterations through group-by groups, so we
    # will emulate it by ordering.
    task_session = None
    for snapshot in snapshots.order_by('task_session__pk', 'time'):
        if not task_session or task_session.pk != snapshot.task_session.pk:
            order_edits, order_executions = 0, 0
            last_edit_snapshot, last_execution_snapshot = None, None
        task_session = snapshot.task_session
        if snapshot.granularity == 'edit':
            order_edits += 1
            snapshot.order = order_edits
            prev_time = last_edit_snapshot.time if last_edit_snapshot else task_session.start
            delta = snapshot.time - prev_time
            snapshot.time_delta = int(delta.total_seconds())
            last_edit_snapshot = snapshot
        else:
            order_executions += 1
            snapshot.order = order_executions
            prev_time = last_execution_snapshot.time if last_execution_snapshot \
                else task_session.start
            delta = snapshot.time - prev_time
            snapshot.time_delta = int(delta.total_seconds())
            last_execution_snapshot= snapshot
        delta_from_start = snapshot.time - task_session.start
        snapshot.time_from_start = int(delta_from_start.total_seconds())
        snapshot.save()


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0058_programsnapshot_time_delta'),
    ]

    operations = [
        migrations.RunPython(
            compute_order_and_time_from_start,
            reverse_code=migrations.RunPython.noop),
    ]

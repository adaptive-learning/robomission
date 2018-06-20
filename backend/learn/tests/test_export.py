import pytest

from learn.export import ProgramSnapshotSerializer
from learn.export import ProgramSnapshotsViewSet
from learn.models import Student, Task, TaskSession, ProgramSnapshot


@pytest.mark.django_db
def test_export_is_fast_enough():
    # Create a lot of ProgramSnapshots
    n_snapshots = 1000
    s = Student.objects.create()
    task = Task.objects.create()
    for i_snapshot in range(n_snapshots):
        ts = TaskSession.objects.create(student=s, task=task)
        ProgramSnapshot.objects.create(task_session=ts, program='frl')

    qs = ProgramSnapshot.objects.prefetch_related('task_session__snapshots').all()
        # +-> TODO: replace by ProgramSnapshotViewSet
    serializer = ProgramSnapshotSerializer(qs, many=True)
    data = serializer.data
    assert len(data) == n_snapshots

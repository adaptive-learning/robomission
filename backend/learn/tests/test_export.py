import pytest

from learn.export import ProgramSnapshotSerializer
from learn.export import ProgramSnapshotsViewSet
from learn.models import Student, Task, TaskSession, ProgramSnapshot


@pytest.mark.slow
@pytest.mark.django_db
def test_export_is_fast_enough():
    # Create a lot of ProgramSnapshots
    #n_snapshots= 500000
    #n_snapshots= 200000
    n_snapshots= 200
    s = Student.objects.create()
    task = Task.objects.create()
    ts = TaskSession.objects.create(student=s, task=task)
    ProgramSnapshot.objects.bulk_create([
        ProgramSnapshot(task_session=ts, program='frl')
        for i_snapshot in range(n_snapshots)
    ])
    qs = ProgramSnapshotsViewSet.queryset
    serializer = ProgramSnapshotSerializer(qs, many=True)
    # Test that serializing the data do not fail
    # (because there are too many of them).
    data = serializer.data
    assert len(data) == n_snapshots

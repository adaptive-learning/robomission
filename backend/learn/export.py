"""Views and utilities for exporting data to csv.
"""
from rest_pandas import PandasViewSet
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, Student, TaskSession, ProgramSnapshot
from learn.serializers import ActionSerializer
from learn.serializers import BlockSerializer
from learn.serializers import LevelSerializer
from learn.serializers import InstructionSerializer
from learn.serializers import ProgramSnapshotSerializer
from learn.serializers import StudentSerializer
from learn.serializers import TaskSerializer
from learn.serializers import TaskSessionSerializer
from learn.serializers import ToolboxSerializer


class BlockViewSet(PandasViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ToolboxViewSet(PandasViewSet):
    queryset = Toolbox.objects.all().prefetch_related('blocks')
    serializer_class = ToolboxSerializer


class LevelViewSet(PandasViewSet):
    serializer_class = LevelSerializer
    queryset = Level.objects.all().prefetch_related('tasks')


class InstructionViewSet(PandasViewSet):
    serializer_class = InstructionSerializer
    queryset = Instruction.objects.all()


class TaskViewSet(PandasViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().select_related('level')


class StudentViewSet(PandasViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TaskSessionsViewSet(PandasViewSet):
    queryset = TaskSession.objects.all()
    serializer_class = TaskSessionSerializer


class ActionsViewSet(PandasViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ProgramSnapshotsViewSet(PandasViewSet):
    queryset = ProgramSnapshot.objects.all()
    serializer_class = ProgramSnapshotSerializer

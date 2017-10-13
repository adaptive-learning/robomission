from django.contrib.auth.models import User
from django.db.models import prefetch_related_objects
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Student, TaskSession
from learn.permissions import IsOwnerOrAdmin
from learn.practice_overview import get_practice_overview
from learn.serializers import BlockSerializer
from learn.serializers import ToolboxSerializer
from learn.serializers import LevelSerializer
from learn.serializers import InstructionSerializer
from learn.serializers import PracticeOverviewSerializer
from learn.serializers import StudentSerializer
from learn.serializers import TaskSerializer
from learn.serializers import TaskSessionSerializer
from learn.serializers import UserSerializer
from learn.world import get_world


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user and user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)


class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ToolboxViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Toolbox.objects.all().prefetch_related('blocks')
    serializer_class = ToolboxSerializer


class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LevelSerializer
    queryset = Level.objects.all().prefetch_related('tasks')


class InstructionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InstructionSerializer
    queryset = Instruction.objects.all()


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().select_related('level')


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    @detail_route(url_path='practice-overview')
    def practice_overview(self, request, pk):
        del request, pk  # not needed
        student = self.get_object()
        prefetch_related_objects(
            [student],
            'seen_instructions', 'task_sessions')
        # -> Same as:
        # student = Student.objects.prefetch_related(
        #       'seen_instructions', 'task_sessions').get(pk=pk)
        world = get_world(include=('instructions', 'levels', 'tasks'))
        overview = get_practice_overview(world, student)
        serializer = PracticeOverviewSerializer(overview)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user and user.is_staff:
            return Student.objects.all()
        return Student.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskSessionsViewSet(viewsets.ModelViewSet):
    queryset = TaskSession.objects.all()
    serializer_class = TaskSessionSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        user = self.request.user
        if user and user.is_staff:
            return TaskSession.objects.all()
        return TaskSession.objects.filter(student=user.student)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)

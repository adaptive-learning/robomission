from django.contrib.auth.models import User
from django.db.models import prefetch_related_objects, Prefetch
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from learn.credits import get_active_credits, get_level_value
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, Student, TaskSession, ProgramSnapshot
from learn.permissions import IsOwnerOrAdmin
from learn.practice_overview import get_practice_overview, get_recommendation
from learn.serializers import ActionSerializer
from learn.serializers import BlockSerializer
from learn.serializers import ToolboxSerializer
from learn.serializers import LevelSerializer
from learn.serializers import InstructionSerializer
from learn.serializers import PracticeOverviewSerializer
from learn.serializers import ProgramSnapshotSerializer
from learn.serializers import StudentSerializer
from learn.serializers import TaskSerializer
from learn.serializers import TaskSessionSerializer
from learn.serializers import UserSerializer
from learn.serializers import RunProgramResponseSerializer
from learn.world import get_world
from learn import actions


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
            'seen_instructions',
            Prefetch('task_sessions', queryset=TaskSession.objects.select_related('task')))
        # -> Same as student = Student.objects.prefetch_related(...).get(pk=pk)
        world = get_world(include=('instructions', 'levels', 'tasks'))
        overview = get_practice_overview(world, student)
        serializer = PracticeOverviewSerializer(overview)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def start_task(self, request, pk=None):
        student = self.get_object()
        assert student.pk == int(pk)
        task_name = request.data['task']
        world = get_world()
        action = actions.start_task(world, student, task_name)
        response_data = {'task_session_id': action.task_session_id}
        return Response(response_data)

    @detail_route(methods=['post'])
    def watch_instruction(self, request, pk=None):
        student = self.get_object()
        assert student.pk == int(pk)
        instruction_name = request.data['instruction']
        world = get_world()
        action = actions.watch_instruction(world, student, instruction_name)
        #serializer = ActionSerializer(action, context={'request': request})
        return Response()

    @detail_route(methods=['post'])
    def edit_program(self, request, pk=None):
        task_session_id = request.data['task-session-id']
        program = request.data['program']
        task_session = (
            TaskSession.objects
            .select_related('task', 'student')
            .get(pk=task_session_id))
        assert task_session.student_id == int(pk)
        world = get_world()
        action = actions.edit_program(world, task_session, program)
        #serializer = ActionSerializer(action, context={'request': request})
        return Response()

    @detail_route(methods=['post'])
    def run_program(self, request, pk=None):
        task_session_id = request.data['task-session-id']
        program = request.data['program']
        correct = request.data['correct']
        task_session = (
            TaskSession.objects
            .select_related('task', 'student')
            .get(pk=task_session_id))
        student = task_session.student
        assert student.pk == int(pk)
        world = get_world()
        action = actions.run_program(world, task_session, program, correct)
        response = {'correct': correct}
        if correct:
            response['recommendation'] = get_recommendation(world, student)
            response['progress'] = {
                'level': get_level_value(world, student),
                'credits': student.credits,
                'active_credits': get_active_credits(world, student)}
        serializer = RunProgramResponseSerializer(response)
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


class ActionsViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ProgramSnapshotsViewSet(viewsets.ModelViewSet):
    queryset = ProgramSnapshot.objects.all()
    serializer_class = ProgramSnapshotSerializer

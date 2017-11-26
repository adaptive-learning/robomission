from django.conf import global_settings, settings
from django.contrib.auth.models import User
from django.db.models import prefetch_related_objects, Prefetch
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from lazysignup.decorators import allow_lazy_user
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from learn.credits import get_active_credits, get_level_value
from learn.models import Block, Toolbox, Level, Task, Instruction
from learn.models import Action, Student, TaskSession, ProgramSnapshot
from learn.models import Feedback
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
from learn.serializers import WorldSerializer
from learn.serializers import RunProgramResponseSerializer
from learn.serializers import FeedbackSerializer
from learn.world import get_world
from learn import actions
from learn import feedback


@ensure_csrf_cookie
@allow_lazy_user
def frontend_app(request, *_):
    try:
        response = render(request, 'index.html')
    except TemplateDoesNotExist as exc:
        raise Exception(
            'Missing index.html template in frontend build directory.\n'
            'Use `make frontend` or `make liveserver`.') from exc
    else:
        delete_invalid_session_cookie_from_response(request, response)
        return response


def delete_invalid_session_cookie_from_response(request, response):
    # In case there is an invalid or otherwise corrupted session id cookie sent
    # from the user, delete the cookie right away. If we ignore invalid
    # session ids, it causes unpredictable problems when running parallel
    # requests from the frontend app as each response will instruct the browser
    # to set a new session id resulting in a race condition.
    if not request.session.session_key:
        return
    if Session.objects.filter(pk=request.session.session_key).exists():
        return
    cookie_name = (
        settings.SESSION_COOKIE_NAME if hasattr(settings, 'SESSION_COOKIE_NAME')
        else global_settings.SESSION_COOKIE_NAME)
    response.delete_cookie(cookie_name)


@allow_lazy_user
def get_or_create_user(request):
    """Return a current user and create one if it doesn't exist

    Lazy user is generally created already when loading the frontend app.
    However, there are at least two cases when the frontend-app view is not
    loaded: one scenario is a manual testing through the browsable api, and
    second is FE development, when the home page is served from the FE server.
    """
    return request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = get_or_create_user(self.request)
        if user and user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

    @list_route(url_path='current')
    def current_user(self, request):
        user = get_or_create_user(request)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class CurrentUserViewSet(viewsets.ViewSet):
    """Phony ViewSet to specify a custom "current_user" entry for the API root.
    """
    # DRF can't derive DjangoModelPermissions for ViewSets without a queryset,
    # so we need to explicitly define them.
    permission_classes = ()

    def list(self, request, format=None):
        return redirect(reverse('user-current', request=request))


class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer


class ToolboxViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Toolbox.objects.all().prefetch_related('blocks')
    serializer_class = ToolboxSerializer


class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LevelSerializer
    queryset = Level.objects.select_related('toolbox').prefetch_related('tasks').all()


class InstructionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InstructionSerializer
    queryset = Instruction.objects.all()


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().select_related('level')


class WorldViewSet(viewsets.ViewSet):
    serializer_class = WorldSerializer
    # DRF can't derive DjangoModelPermissions for ViewSets without a queryset,
    # so we need to explicitly define them.
    permission_classes = ()

    def list(self, request, format=None):
        world = get_world()
        serializer = WorldSerializer(world, context={'request': request})
        return Response(serializer.data)


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsOwnerOrAdmin,)

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
        action = actions.edit_program(task_session, program)
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
        action = actions.run_program(task_session, program, correct)
        world = get_world()
        response = {'correct': correct}
        if correct:
            prefetch_related_objects(
                [student],
                Prefetch(
                    'task_sessions',
                    queryset=TaskSession.objects.select_related('task')))
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

    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)


class TaskSessionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskSession.objects.all()
    serializer_class = TaskSessionSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def get_queryset(self):
        user = self.request.user
        if user and user.is_staff:
            return TaskSession.objects.all()
        return TaskSession.objects.filter(student=user.student)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)


class ActionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ProgramSnapshotsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProgramSnapshot.objects.all()
    serializer_class = ProgramSnapshotSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsOwnerOrAdmin,)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated() else None
        new_feedback = serializer.save(user=user)
        feedback.log_and_send(new_feedback)

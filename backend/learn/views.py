from django.conf import global_settings, settings
from django.contrib.auth.models import User
from django.db.models import prefetch_related_objects, Prefetch
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from learn.mastery import get_level
from learn.domain import get_domain
from learn.models import TaskSession, Student, Teacher
from learn.permissions import IsOwnerOrAdmin, IsOwnerOrAdminOrReadOnly
from learn.practice_overview import get_practice_overview, get_recommendation
from learn.serializers import DomainSerializer
from learn.serializers import PracticeOverviewSerializer
from learn.serializers import StudentSerializer
from learn.serializers import UserSerializer
from learn.serializers import RunProgramResponseSerializer
from learn.serializers import TeacherSerializer
from learn.users import get_or_fake_user, create_user_student
from learn import actions


@ensure_csrf_cookie
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



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)

    @list_route(url_path='current')
    def current_user(self, request):
        user = get_or_fake_user(request)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @list_route(url_path='create')
    @create_user_student
    def create_user(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class CurrentUserViewSet(viewsets.ViewSet):
    """Phony ViewSet to specify a custom "current_user" entry for the API root.
    """
    # DRF can't derive DjangoModelPermissions for ViewSets without a queryset,
    # so we need to explicitly define them.
    permission_classes = ()

    def list(self, request, format=None):
        return redirect(reverse('user-current', request=request))


class DomainViewSet(viewsets.ViewSet):
    serializer_class = DomainSerializer
    # DRF can't derive DjangoModelPermissions for ViewSets without a queryset,
    # so we need to explicitly define them.
    permission_classes = ()

    def list(self, request, format=None):
        domain = get_domain()
        # TODO: Don't pass request context if not needed.
        serializer = DomainSerializer(domain, context={'request': request})
        return Response(serializer.data)


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsOwnerOrAdmin,)


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)

    @detail_route(url_path='practice-overview')
    def practice_overview(self, request, pk):
        del request, pk  # not needed
        student = self.get_object()
        prefetch_related_objects(
            [student],
            Prefetch(
                'task_sessions',
                queryset=TaskSession.objects.select_related('task')))
        # -> Same as student = Student.objects.prefetch_related(...).get(pk=pk)
        domain = get_domain()
        overview = get_practice_overview(domain, student)
        serializer = PracticeOverviewSerializer(overview)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def start_task(self, request, pk=None):
        student = self.get_object()
        assert student.pk == int(pk)
        task_name = request.data['task']
        domain = get_domain()
        action = actions.start_task(domain, student, task_name)
        response_data = {'task_session_id': action.task_session_id}
        return Response(response_data)

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
        domain = get_domain()
        progress = actions.run_program(domain, task_session, program, correct)
        response = {'correct': correct}
        if correct:
            prefetch_related_objects(
                [student],
                Prefetch(
                    'task_sessions',
                    queryset=TaskSession.objects.select_related('task')))
            response['recommendation'] = get_recommendation(domain, student)
            response['progress'] = progress or []
            print('progress', progress)
        serializer = RunProgramResponseSerializer(response)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def watch_instruction(self, request, pk=None):
        student = self.get_object()
        assert student.pk == int(pk)
        instruction_name = request.data['instruction']
        domain = get_domain()
        action = actions.watch_instruction(domain, student, instruction_name)
        #serializer = ActionSerializer(action, context={'request': request})
        return Response()

    def get_queryset(self):
        user = get_or_fake_user(self.request)
        return Student.objects.filter(user=user)

    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)

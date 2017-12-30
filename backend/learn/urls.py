from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from learn import export
from learn import views


api_router = DefaultRouter()
#api_router.register(r'blocks', views.BlockViewSet)
#api_router.register(r'toolboxes', views.ToolboxViewSet)
#api_router.register(r'levels', views.LevelViewSet)
#api_router.register(r'instructions', views.InstructionViewSet)
#api_router.register(r'tasks', views.TaskViewSet)
#api_router.register(r'teachers', views.TeacherViewSet, base_name='teacher')
#api_router.register(r'task_sessions', views.TaskSessionsViewSet, base_name='tasksession')
#api_router.register(r'program_snapshots', views.ProgramSnapshotsViewSet, base_name='programsnapshot')
#api_router.register(r'actions', views.ActionsViewSet, base_name='action')
api_router.register(r'users', views.UserViewSet, base_name='user')
#api_router.register(r'current_user', views.CurrentUserViewSet, base_name='current_user')
api_router.register(r'students', views.StudentViewSet, base_name='student')
api_router.register(r'world', views.WorldViewSet, base_name='world')
api_router.register(r'feedback', views.FeedbackViewSet, base_name='feedback')


export_router = DefaultRouter()
export_router.register(
    r'latest/bundle',
    export.LatestBundleViewSet,
    base_name='latest/bundle')
export_router.register(r'current/blocks', export.BlockViewSet)
export_router.register(r'current/toolboxes', export.ToolboxViewSet)
export_router.register(r'current/levels', export.LevelViewSet)
export_router.register(r'current/instructions', export.InstructionViewSet)
export_router.register(r'current/tasks', export.TaskViewSet)
export_router.register(r'current/students', export.StudentViewSet)
export_router.register(r'current/task_sessions', export.TaskSessionsViewSet)
export_router.register(r'current/program_snapshots', export.ProgramSnapshotsViewSet)
export_router.register(r'current/actions', export.ActionsViewSet)


urlpatterns = [
    url(r'^api/', include(api_router.urls)),
    url(r'^export/', include(export_router.urls, namespace='export')),
]

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from learn import export
from learn import views


apiRouter = DefaultRouter()
apiRouter.register(r'blocks', views.BlockViewSet)
apiRouter.register(r'toolboxes', views.ToolboxViewSet)
apiRouter.register(r'levels', views.LevelViewSet)
apiRouter.register(r'instructions', views.InstructionViewSet)
apiRouter.register(r'tasks', views.TaskViewSet)
apiRouter.register(r'users', views.UserViewSet)
apiRouter.register(r'students', views.StudentViewSet, base_name='student')
apiRouter.register(r'task_sessions', views.TaskSessionsViewSet, base_name='tasksession')
apiRouter.register(r'program_snapshots', views.ProgramSnapshotsViewSet, base_name='programsnapshot')
apiRouter.register(r'actions', views.ActionsViewSet, base_name='action')
apiRouter.register(r'current_user', views.CurrentUserViewSet, base_name='current_user')
apiRouter.register(r'world', views.WorldViewSet, base_name='world')
apiRouter.register(r'feedback', views.FeedbackViewSet, base_name='feedback')


exportRouter = DefaultRouter()
exportRouter.register(
    r'latest/bundle',
    export.LatestBundleViewSet,
    base_name='latest/bundle')
exportRouter.register(r'current/blocks', export.BlockViewSet)
exportRouter.register(r'current/toolboxes', export.ToolboxViewSet)
exportRouter.register(r'current/levels', export.LevelViewSet)
exportRouter.register(r'current/instructions', export.InstructionViewSet)
exportRouter.register(r'current/tasks', export.TaskViewSet)
exportRouter.register(r'current/students', export.StudentViewSet)
exportRouter.register(r'current/task_sessions', export.TaskSessionsViewSet)
exportRouter.register(r'current/program_snapshots', export.ProgramSnapshotsViewSet)
exportRouter.register(r'current/actions', export.ActionsViewSet)


urlpatterns = [
    url(r'^api/', include(apiRouter.urls)),
    url(r'^export/', include(exportRouter.urls, namespace='export')),
]

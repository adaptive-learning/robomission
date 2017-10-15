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


exportRouter = DefaultRouter()
exportRouter.register(r'blocks', export.BlockViewSet)
exportRouter.register(r'toolboxes', export.ToolboxViewSet)
exportRouter.register(r'levels', export.LevelViewSet)
exportRouter.register(r'instructions', export.InstructionViewSet)
exportRouter.register(r'tasks', export.TaskViewSet)
exportRouter.register(r'students', export.StudentViewSet)
exportRouter.register(r'task_sessions', export.TaskSessionsViewSet)
exportRouter.register(r'program_snapshots', export.ProgramSnapshotsViewSet)
exportRouter.register(r'actions', export.ActionsViewSet)


urlpatterns = [
    url(r'^api/', include(apiRouter.urls)),
    url(r'^export/', include(exportRouter.urls, namespace='export')),
]

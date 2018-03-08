from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from learn import export
from learn import views


api_router = DefaultRouter()
api_router.register(r'domain', views.DomainViewSet, base_name='domain')
api_router.register(r'users', views.UserViewSet, base_name='user')
api_router.register(r'students', views.StudentViewSet, base_name='student')
#api_router.register(r'teachers', views.TeacherViewSet, base_name='teacher')
#api_router.register(r'current_user', views.CurrentUserViewSet, base_name='current_user')


export_router = DefaultRouter()
export_router.register(
    r'latest/bundle',
    export.LatestBundleViewSet,
    base_name='latest/bundle')
export_router.register(r'current/blocks', export.BlockViewSet)
export_router.register(r'current/toolboxes', export.ToolboxViewSet)
export_router.register(r'current/tasks', export.TaskViewSet)
export_router.register(r'current/students', export.StudentViewSet)
export_router.register(r'current/task_sessions', export.TaskSessionsViewSet)
export_router.register(r'current/program_snapshots', export.ProgramSnapshotsViewSet)
export_router.register(r'current/actions', export.ActionsViewSet)


urlpatterns = [
    url(r'^api/', include(api_router.urls)),
    url(r'^export/', include(export_router.urls, namespace='export')),
]
